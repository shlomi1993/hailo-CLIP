import subprocess

from play_lullaby import play_mp3


def notify(message: str) -> None:
    print(f"Notification: {message}")
    # msg = f"curl -X POST http://<IP>:5001/notify  -H \"Content-Type: application/json\"  -d '{{\"message\":\"{message}\"}}'"
    # subprocess.run(msg.split())


BEHAVIOR_DICT = {
    # Cry detection
    "Calm baby": play_mp3(),
    "Crying baby": play_mp3(),

    # Sleep detection
    "awaken baby": play_mp3(),
    "sleeping baby": play_mp3(),

    # Hazard detection
    "knife": notify("\nKnife detected\n"),
    "scissors": notify("\Scissors detected\n"),
    "gun": notify("\nGun detected\n"),
    "glass": notify("\nGlass detected\n"),
    "rubber": notify("\nRubber detected\n")
}


def handle_match(match: str) -> None:
    handler = BEHAVIOR_DICT.get(match)
    if handler:
        handler()
    else:
        print(f"No handler for match: {match}")
