import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 817761548  # Tukar kepada Telegram ID admin jika perlu.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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

BUTTON_OR = "OR"
BUTTON_GE = "GE"
BUTTON_ADMIN = "Admin"
BUTTON_BACK = "Back"
BUTTON_DATE_INFO = "DATE INFO"
