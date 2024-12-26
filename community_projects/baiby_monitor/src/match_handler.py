from community_projects.baiby_monitor.src.play_lullaby import play_mp3
from community_projects.baiby_monitor.src.baiby_telegram import send_telegram_message


class MatchHandler:
    _instance = None

    BEHAVIOR_DICT = {
        # Cry detection
        "Calm baby": None,
        "Crying baby": (play_mp3, []),

        # Sleep detection
        "awaken baby": (play_mp3, []),
        "sleeping baby": None,

        # Hazard detection
        "knife": (send_telegram_message, ["knife detected"]),
        "scissors": (send_telegram_message, ["scissors detected"]),
        "gun": (send_telegram_message, ["gun detected"]),
        "glass": (send_telegram_message, ["glass detected"]),
        "rubber": (send_telegram_message, ["rubber detected"])
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MatchHandler, cls).__new__(cls)
        return cls._instance

    def handle(self, label: str) -> None:
        behavior_tuple = self.BEHAVIOR_DICT.get(label)
        if behavior_tuple:
            func, args = behavior_tuple
            func(*args)
