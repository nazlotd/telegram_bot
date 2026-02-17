import os

from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# GLOBAL DATA
DATA = {
    "OR":{},
    "GE":{}
}

# ================= CONFIG =================
TOKEN = "8562970237:AAFrGeiWBr1dLl1dDM6DYEAsOcUrQIWBwHE"
ADMIN_ID = 817761548  # 👈 tukar ke Telegram ID admin

BASE_DIR = "data"

OR_DATA = {
    "1": {
        "images": ["OR/or1_a.jpeg", "OR/or1_b.jpeg"],
        "title": "OR 1",
        "start": "23/01/2026",
        "end": "25/02/2026"
    },
    "2": {
        "images": ["OR/or2_a.jpeg", "OR/or2_b.jpeg"],
        "title": "OR 2",
        "start": "01/01/2026",
        "end": "28/02/2026"
    },
    "3": {
        "images": ["OR/or3_a.jpeg", "OR/or3_b.jpeg"],
        "title": "OR 3",
        "start": "13/02/2026",
        "end": "12/03/2026"
    },
    "4": {
        "images": ["OR/or4_a.jpeg", "OR/or4_b.jpeg"],
        "title": "OR 4",
        "start": "13/02/2026",
        "end": "12/03/2026"
    },
    "5": {
        "images": ["OR/or5_a.jpeg", "OR/or5_b.jpeg"],
        "title": "OR 5",
        "start": "01/01/2026",
        "end": "30/02/2026"
    }
}

GE_DATA = {
    "1": {
        "images": ["GE/ge1_a.jpeg", "GE/ge1_b.jpeg"],
        "title": "GE 1",
        "start": "23/01/2026",
        "end": "25/02/2026"
    },
    "2": {
        "images": ["GE/ge2_a.jpeg", "GE/ge2_b.jpeg"],
        "title": "GE 2",
        "start": "01/02/2026",
        "end": "28/02/2026"
    },
    "3": {
        "images": ["GE/ge3_a.jpeg", "GE/ge3_b.jpeg"],
        "title": "GE 3",
        "start": "16/01/2026",
        "end": "12/02/2026"
    },
    "4": {
        "images": ["GE/ge4_a.jpeg", "GE/ge4_b.jpeg"],
        "title": "GE 4",
        "start": "01/03/2026",
        "end": "31/03/2026"
    },
    "5": {
        "images": ["GE/ge5_a.jpeg", "GE/ge5_b.jpeg"],
        "title": "GE 5",
        "start": "01/04/2026",
        "end": "30/04/2026"
    }
}

STANDEE_DATA = {
    "1": {  
        "images": ["data/STANDEE/test1.jpeg"],
        "title": "TEST 1",
    },
    "2": {  
        "images": ["data/STANDEE/test2.jpeg"],
        "title": "TEST 2",
    },
    "3": {  
        "images": ["data/STANDEE/test3.jpeg"],
        "title": "TEST 3",
    },
    "4": {  
        "images": ["data/STANDEE/test4.jpeg"],
        "title": "TEST 4",
    },
    "5": {  
        "images": ["data/STANDEE/test5.jpeg"],
        "title": "TEST 5"
    }

}

# ================= KEYBOARDS =================
MAIN_MENU = ReplyKeyboardMarkup(
    [["OR", "GE"], ["👑 Admin"]],
    resize_keyboard=True
)

BACK_MENU = ReplyKeyboardMarkup(
    [["⬅️ Back"]],
    resize_keyboard=True
)

ADMIN_MENU = ReplyKeyboardMarkup(
    [
        ["UPDATE OR", "UPDATE GE"],
        ["⬅ Back"]
    ],
    resize_keyboard=True
)

# ================= FUNCTIONS =================

def get_main_menu(user_id):
    buttons = [
        ["📁 OR", "📁 GE"],
        ["4 RM10_PERAYAAN", "STANDEE"]
    ]

    if user_id == ADMIN_ID:
        buttons.append(["👑 Admin"])

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    intro_path = "data/intro.jpeg"

    if os.path.exists(intro_path):
        with open(intro_path, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption="🤖 Welcome ini hanya test dari Nazs."
            )
    else:
        await update.message.reply_text(
            "🤖 Welcome to OR & GE Bot\n\nSila pilih kategori di bawah."
        )

    # Lepas intro → baru tunjuk menu
    await update.message.reply_text(
        "Main Menu:",
    reply_markup=get_main_menu(update.effective_user.id)
    )

async def show_or_menu(update, context):
    buttons = [[f"OR {k}"] for k in OR_DATA]
    buttons.append(["⬅️ Back"])
    await update.message.reply_text(
        "📁 OR LIST",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )

async def show_ge_menu(update, context):
    buttons = [[f"GE {k}"] for k in GE_DATA]
    buttons.append(["⬅️ Back"])
    await update.message.reply_text(
        "📁 GE LIST",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )

async def show_admin_menu(update, context):
    await update.message.reply_text(
        "🔥 Admin Panel",
        reply_markup=ADMIN_MENU
    )

async def send_images(update, context, data):
    chat_id = update.effective_chat.id
    media = []

    caption = (
        f"📌 {data['title']}\n"
        f"📅 Effective Period:\n"
        f"{data['start']} – {data['end']}"
    )

    for i, img in enumerate(data["images"]):
        path = os.path.join(BASE_DIR, img)
        if os.path.exists(path):
            if i == 0:
                media.append(InputMediaPhoto(open(path, "rb"), caption=caption, parse_mode="Markdown"))
            else:
                media.append(InputMediaPhoto(open(path, "rb")))

    await context.bot.send_media_group(chat_id=chat_id, media=media)

async def show_main_menu(update, context):
    await update.message.reply_text(
        "Main Menu:",
        reply_markup=get_main_menu(update.effective_user.id)
    )

# ================= MESSAGE HANDLER =================
async def handle_message(update, context):
    msg = update.message.text.strip() if update.message.text else ""
    user_id = update.effective_user.id

    # BACK (WAJIB PALING ATAS)
    if msg.endswith("Back"):
        await show_main_menu(update, context)
        return

    # ADMIN
    if msg == "👑 Admin":
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ No access")
            return
        await show_admin_menu(update, context)
        return

    # ==============================
    # BUTTON TRIGGER
    # ==============================

    if msg == "UPDATE OR":
        context.user_data["category"] = "OR"
        context.user_data["mode"] = "select_number"
        await update.message.reply_text("OR nombor berapa?")
        return

    if msg == "UPDATE GE":
        context.user_data["category"] = "GE"
        context.user_data["mode"] = "select_number"
        await update.message.reply_text("GE nombor berapa?")
        return

    # ADMIN STATE MACHINE

    mode = context.user_data.get("mode")

    # ---------- STEP 1: SELECT NUMBER ----------
    if mode == "select_number":
        if msg and msg.isdigit():
            context.user_data["item"] = msg
            context.user_data["mode"] = "image_a"
            await update.message.reply_text("Upload Gambar A")
        else:
            await update.message.reply_text("Sila masukkan nombor yang sah.")
        return


    # ---------- STEP 2: IMAGE A ----------
    if mode == "image_a":
        if update.message.photo:
            photo = update.message.photo[-1]
            file = await photo.get_file()

            folder = context.user_data["category"]  # OR / GE
            item = context.user_data["item"]

            path = f"data/{folder}/{item}_a.jpg"
            await file.download_to_drive(path)

            context.user_data["mode"] = "image_b"
            await update.message.reply_text("Upload Gambar B")
        else:
            await update.message.reply_text("Sila upload gambar.")
        return


    # ---------- STEP 3: IMAGE B ----------
    if mode == "image_b":
        if update.message.photo:
            photo = update.message.photo[-1]
            file = await photo.get_file()

            folder = context.user_data["category"]
            item = context.user_data["item"]

            path = f"data/{folder}/{item}_b.jpg"
            await file.download_to_drive(path)

            context.user_data["mode"] = "start_date"
            await update.message.reply_text("Masukkan tarikh START (YYYY-MM-DD)")
        else:
            await update.message.reply_text("Sila upload gambar.")
        return


    # ---------- STEP 4: START DATE ----------
    if mode == "start_date":
        context.user_data["start_date"] = msg
        context.user_data["mode"] = "end_date"
        await update.message.reply_text("Masukkan tarikh END (YYYY-MM-DD)")
        return


    # ---------- STEP 5: END DATE ----------
    if mode == "end_date":
        context.user_data["end_date"] = msg

        # Save to your data structure
        folder = context.user_data["category"]
        item = context.user_data["item"]

        # contoh simpan ke dict
        if item not in DATA[folder]:
            DATA[folder][item] = {}

        DATA[folder][item]["start"] = context.user_data["start_date"]
        DATA[folder][item]["end"] = context.user_data["end_date"]

        await update.message.reply_text("✅ Update berjaya!")

        context.user_data.clear()
        return

    # MAIN MENU
    if msg == "📁 OR":
        await show_or_menu(update, context)
        return

    if msg == "📁 GE":
        await show_ge_menu(update, context)
        return

    # 4 RM10 + PERAYAAN
    if msg == "4 RM10_PERAYAAN":
        image_path = "data/4 RM10_PERAYAAN.jpeg"

        if os.path.exists(image_path):
            with open(image_path, "rb") as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption="4 RM10_PERAYAAN"
                )
            return
        else:
            await update.message.reply_text("❌ Gambar tidak dijumpai.")
            return

    # STANDEE
    if msg == "STANDEE":
            buttons = [[k] for k in STANDEE_DATA.keys()]
            buttons.append(["⬅ Back"])
            await update.message.reply_text(
                "Pilih Standee:",
                reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            )
            return
    
    if msg in STANDEE_DATA:
        data = STANDEE_DATA[msg]

        for img in data["images"]:
            if os.path.exists(img):
                with open(img, "rb") as photo:
                    await update.message.reply_photo(
                    photo=photo,
                    caption=data["title"]
                    )
            else:
                await update.message.reply_text("❌ Gambar tidak dijumpai.")
            return

    # OR ITEM
    if msg.startswith("OR "):
        parts = msg.split(" ", 1)
        if len(parts) != 2:
            await update.message.reply_text("❌ Format salah")
            return

        key = parts[1]
        if key in OR_DATA:
            await send_images(update, context, OR_DATA[key])
        else:
            await update.message.reply_text("❌ OR tidak wujud")
        return

    # GE ITEM
    if msg.startswith("GE "):
        parts = msg.split(" ", 1)
        if len(parts) != 2:
            await update.message.reply_text("❌ Format salah")
            return

        key = parts[1]
        if key in GE_DATA:
            await send_images(update, context, GE_DATA[key])
        else:
            await update.message.reply_text("❌ GE tidak wujud")
        return

    # ===== FALLBACK =====
    if not context.user_data.get("mode"):
        await update.message.reply_text(
        "! Arahan tidak dikenali.\nSila pilih menu.",
    reply_markup=get_main_menu(update.effective_user.id)
    )
        return

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(~filters.COMMAND, handle_message))
    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()