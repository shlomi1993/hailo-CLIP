import subprocess

from play_lullaby import play_mp3


def notify(message: str) -> None:
    msg = f"curl -X POST http://<IP>:5001/notify  -H \"Content-Type: application/json\"  -d '{{\"message\":\"{message}\"}}'"
    subprocess.run(msg.split())


BEHAVIOR_DICT = {
    # Cry detection
    "Calm baby": "",
    "Crying baby": play_mp3(),

    # Sleep detection
    "awaken baby": play_mp3(),
    "sleeping baby": "",

    # Hazard detection
    "knife": notify(),
    "scissors": "",
    "gun": "",
    "glass": "",
    "rubber": ""
}


def handle_match(match: str) -> None:
    handler = BEHAVIOR_DICT.get(match)
    if handler:
        handler()
    else:
        print(f"No handler for match: {match}")
