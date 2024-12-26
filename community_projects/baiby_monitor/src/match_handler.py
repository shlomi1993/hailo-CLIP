import subprocess

from play_lullaby import play_mp3
from baiby_telegram import send_telegram_message
from multiprocessing import Process, Queue


BEHAVIOR_DICT = {
    # Cry detection
    "Calm baby": None,
    "Crying baby": play_mp3(),

    # Sleep detection
    "awaken baby": play_mp3(),
    "sleeping baby": play_mp3(),

    # Hazard detection
    "knife": send_telegram_message("Knife detected\n"),
    "scissors": send_telegram_message("Scissors detected\n"),
    "gun": send_telegram_message("Gun detected\n"),
    "glass": send_telegram_message("Glass detected\n"),
    "rubber": send_telegram_message("Rubber detected\n")
}


def handle_match(match: str) -> None:
    handler = BEHAVIOR_DICT.get(match)
    subprocess.r
    if handler:
        handler()
