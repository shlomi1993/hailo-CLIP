import os
import argparse
import logging
import sys
import signal
import importlib.util
from functools import partial
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst, GLib
from clip_app.logger_setup import setup_logger, set_log_level
from clip_app.clip_pipeline import get_pipeline
from clip_app.text_image_matcher import text_image_matcher
from clip_app import gui

# add logging
logger = setup_logger()
set_log_level(logger, logging.INFO)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Hailo online CLIP app")
    parser.add_argument("--input", "-i", type=str, default="/dev/video0", help="URI of the input stream. Default is /dev/video0. Use '--input demo' to use the demo video.")
    parser.add_argument("--detector", "-d", type=str, choices=["person", "face", "none"], default="none", help="Which detection pipeline to use.")
    parser.add_argument("--json-path", type=str, default=None, help="Path to JSON file to load and save embeddings. If not set, embeddings.json will be used.")
    parser.add_argument("--disable-sync", action="store_true",help="Disables display sink sync, will run as fast as possible. Relevant when using file source.")
    parser.add_argument("--dump-dot", action="store_true", help="Dump the pipeline graph to a dot file.")
    parser.add_argument("--detection-threshold", type=float, default=0.5, help="Detection threshold.")
    parser.add_argument("--show-fps", "-f", action="store_true", help="Print FPS on sink.")
    parser.add_argument("--enable-callback", action="store_true", help="Enables the use of the callback function.")
    parser.add_argument("--callback-path", type=str, default=None, help="Path to the custom user callback file.")
    parser.add_argument("--disable-runtime-prompts", action="store_true", help="When set, app will not support runtime prompts. Default is False.")

    return parser.parse_args()

def load_custom_callback(callback_path=None):
    if callback_path:
        spec = importlib.util.spec_from_file_location("custom_callback", callback_path)
        custom_callback = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(custom_callback)
    else:
        import clip_app.user_callback as custom_callback
    return custom_callback

def on_destroy(window):
    logger.info("Destroying window...")
    window.quit_button_clicked(None)


def main():
    args = parse_arguments()
    custom_callback_module = load_custom_callback(args.callback_path)
    app_callback = custom_callback_module.app_callback
    app_callback_class = custom_callback_module.app_callback_class
    
    logger = setup_logger()
    set_log_level(logger, logging.INFO)
    
    user_data = app_callback_class()
    win = AppWindow(args, user_data, app_callback)
    win.connect("destroy", on_destroy)
    win.show_all()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()

class AppWindow(Gtk.Window):
    # Add GUI functions to the AppWindow class
    build_ui = gui.build_ui
    add_text_boxes = gui.add_text_boxes
    update_text_boxes = gui.update_text_boxes
    update_text_prefix = gui.update_text_prefix
    quit_button_clicked = gui.quit_button_clicked
    on_text_box_updated = gui.on_text_box_updated
    on_slider_value_changed = gui.on_slider_value_changed
    on_negative_check_button_toggled = gui.on_negative_check_button_toggled
    on_ensemble_check_button_toggled = gui.on_ensemble_check_button_toggled
    on_load_button_clicked = gui.on_load_button_clicked
    on_save_button_clicked = gui.on_save_button_clicked
    update_progress_bars = gui.update_progress_bars
    on_track_id_update = gui.on_track_id_update
    disable_text_boxes = gui.disable_text_boxes

    # Add the get_pipeline function to the AppWindow class
    get_pipeline = get_pipeline
    

    def __init__(self, args, user_data, app_callback):
        Gtk.Window.__init__(self, title="Clip App")
        self.set_border_width(10)
        self.set_default_size(1, 1)
        self.fullscreen_mode = False

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        # move self.current_path one directory up to get the path to the workspace
        self.current_path = os.path.dirname(self.current_path)
        os.environ["GST_DEBUG_DUMP_DOT_DIR"] = self.current_path

        self.tappas_postprocess_dir = os.environ.get('TAPPAS_POST_PROC_DIR', '')
        if self.tappas_postprocess_dir == '':
            logger.error("TAPPAS_POST_PROC_DIR environment variable is not set. Please set it by sourcing setup_env.sh")
            sys.exit(1)

        self.dump_dot = args.dump_dot
        self.sync_req = 'false' if args.disable_sync else 'true'
        self.show_fps = args.show_fps
        self.enable_callback = args.enable_callback or args.callback_path is not None
        self.json_file = os.path.join(self.current_path, "embeddings.json") if args.json_path is None else args.json_path
        if args.input == "demo":
            self.input_uri = os.path.join(self.current_path, "resources", "clip_example.mp4")
            self.json_file = os.path.join(self.current_path, "example_embeddings.json") if args.json_path is None else args.json_path
        else:
            self.input_uri = args.input
        self.detector = args.detector
        self.user_data = user_data
        self.app_callback = app_callback
        # get current path
        Gst.init(None)
        self.pipeline = self.create_pipeline()
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

        # get xvimagesink element and disable qos
        # xvimagesink is instantiated by fpsdisplaysink
        hailo_display = self.pipeline.get_by_name("hailo_display")
        xvimagesink = hailo_display.get_by_name("xvimagesink0")
        xvimagesink.set_property("qos", False)

        # get text_image_matcher instance
        self.text_image_matcher = text_image_matcher
        self.text_image_matcher.set_threshold(args.detection_threshold)

        # build UI
        self.build_ui(args)

        # set runtime
        if args.disable_runtime_prompts:
            logger.info("No text embedding runtime selected, adding new text is disabled. Loading %s", self.json_file)
            self.disable_text_boxes()
            self.on_load_button_clicked(None)
        else:
            self.text_image_matcher.init_clip()

        if self.text_image_matcher.model_runtime is not None:
            logger.info("Using %s for text embedding", self.text_image_matcher.model_runtime)
            self.on_load_button_clicked(None)

        # Connect pad probe to the identity element
        if self.enable_callback:
            identity = self.pipeline.get_by_name("identity_callback")
            if identity is None:
                logger.warning("identity_callback element not found, add <identity name=identity_callback> in your pipeline where you want the callback to be called.")
            else:
                identity_pad = identity.get_static_pad("src")
                identity_pad.add_probe(Gst.PadProbeType.BUFFER, partial(self.app_callback, self), self.user_data)
        # start the pipeline
        self.pipeline.set_state(Gst.State.PLAYING)

        if self.dump_dot:
            GLib.timeout_add_seconds(5, self.dump_dot_file)

        self.update_text_boxes()

        # Define a timeout duration in nanoseconds (e.g., 5 seconds)
        timeout_ns = 5 * Gst.SECOND

        # Wait until state change is done or until the timeout occurs
        state_change_return, _state, _pending = self.pipeline.get_state(timeout_ns)

        if state_change_return == Gst.StateChangeReturn.SUCCESS:
            logger.info("Pipeline state changed to PLAYING successfully.")
        elif state_change_return == Gst.StateChangeReturn.ASYNC:
            logger.info("State change is ongoing asynchronously.")
        elif state_change_return == Gst.StateChangeReturn.FAILURE:
            logger.info("State change failed.")
        else:
            logger.warning("Unknown state change return value.")


    def dump_dot_file(self):
        logger.info("Dumping dot file...")
        Gst.debug_bin_to_dot_file(self.pipeline, Gst.DebugGraphDetails.ALL, "pipeline")
        return False


    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.on_eos()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            logger.error("Error: %s %s", err, debug)
            self.shutdown()
        # print QOS messages
        elif t == Gst.MessageType.QOS:
            # print which element is reporting QOS
            src = message.src.get_name()
            logger.info("QOS from %s", src)
        return True


    def on_eos(self):
        logger.info("EOS received, shutting down the pipeline.")
        self.pipeline.set_state(Gst.State.PAUSED)
        GLib.usleep(100000)  # 0.1 second delay

        self.pipeline.set_state(Gst.State.READY)
        GLib.usleep(100000)  # 0.1 second delay

        self.pipeline.set_state(Gst.State.NULL)
        GLib.idle_add(Gtk.main_quit)

    def shutdown(self):
        logger.info("Sending EOS event to the pipeline...")
        self.pipeline.send_event(Gst.Event.new_eos())

    def create_pipeline(self):
        pipeline_str = get_pipeline(self)
        logger.info('PIPELINE:\ngst-launch-1.0 %s', pipeline_str)
        try:
            pipeline = Gst.parse_launch(pipeline_str)
        except GLib.Error as e:
            logger.error("An error occurred while parsing the pipeline: %s", e)
        return pipeline

if __name__ == "__main__":
    main()
