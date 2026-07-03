import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_env_file(path=os.path.join(BASE_DIR, ".env")):
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key and key not in os.environ:
                os.environ[key] = value


load_env_file()

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 817761548  # Tukar kepada Telegram ID admin jika perlu.

DATA_DIR = os.getenv("DATA_DIR", os.path.join(BASE_DIR, "data"))
DATA_FILE = os.path.join(DATA_DIR, "data.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
INTRO_FILE = os.getenv("INTRO_FILE", os.path.join(BASE_DIR, "data", "intro.jpeg"))
INTRO_ANIMATION_FILE = os.getenv(
    "INTRO_ANIMATION_FILE",
    os.path.join(BASE_DIR, "data", "intro.mp4"),
)
INTRO_GIF_FILE = os.getenv(
    "INTRO_GIF_FILE",
    os.path.join(BASE_DIR, "data", "intro.gif"),
)

CATEGORY_OR = "OR"
CATEGORY_GE = "GE"
CATEGORY_STANDEE = "STANDEE"
CATEGORY_4_RM10 = "4 RM10_PERAYAAN"
CATEGORIES = (CATEGORY_OR, CATEGORY_GE, CATEGORY_STANDEE, CATEGORY_4_RM10)

ITEM_COUNTER_AB = "COUNTER A/B"
ITEM_P_WING = "P.WING"
ITEM_CAT = "CAT"
ITEM_DETTOL = "DETTOL"
ITEM_DUTH_LADY = "DUTH LADY"
STANDEE_ITEMS = (ITEM_CAT, ITEM_DETTOL, ITEM_DUTH_LADY)

BUTTON_OR = "OR"
BUTTON_GE = "GE"
BUTTON_ADMIN = "Admin"
BUTTON_BACK = "⬅️ Back"
BUTTON_DATE_INFO = "DATE INFO"
BUTTON_COUNTER_PWING_STANDEE = "COUNTER A,B / P.WING / STANDEE"
