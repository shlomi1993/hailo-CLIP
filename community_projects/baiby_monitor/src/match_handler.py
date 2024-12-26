from community_projects.baiby_monitor.src.play_lullaby import play_mp3
from community_projects.baiby_monitor.src.baiby_telegram import send_telegram_message


_g_crying = False
_g_sleeping = False


def set_crying(is_crying: bool) -> None:
    global _g_crying
    _g_crying = is_crying


def set_sleeping(is_sleeping: bool) -> None:
    global _g_sleeping
    _g_sleeping = is_sleeping


class MatchHandler:
    _instance = None

    BEHAVIOR_DICT = {
        # Cry detection
        "Happy baby": (set_crying, [False]),
        "Crying baby": (set_crying, [True]),

        # Sleep detection
        "awaken baby": (set_sleeping, [False]),
        "sleeping baby": (set_sleeping, [True]),
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

            print(f"Now baby is {'crying' if _g_crying else 'not crying'} and {'sleeping' if _g_sleeping else 'not sleeping'}")
