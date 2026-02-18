import os
import json
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 817761548
BASE_DIR = "data"
DATA_FILE = os.path.join(BASE_DIR, "data.json")
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

# ================= LOAD / SAVE =================

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"OR": {}, "GE": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def format_date(date_str):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return d.strftime("%d/%m/%Y")
    except:
        return date_str


# ================= MENUS =================

def get_main_menu(user_id):
    keyboard = [
        ["📂 OR", "📂 GE"],
        ["STANDEE"]
    ]
    if user_id == ADMIN_ID:
        keyboard.append(["👑 Admin"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_admin_menu():
    keyboard = [
        ["UPDATE OR", "UPDATE GE"],
        ["⬅ Back"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("START TRIGGERED")
    await update.message.reply_text("Bot aktif")

# ================= SEND ITEM =================

async def send_item(update, context, category, key):
    data = load_data()

    if key not in data[category]:
        await update.message.reply_text("❌ Item tidak wujud")
        return

    item = data[category][key]

    media = []
    for img in item["images"]:
        path = os.path.join(BASE_DIR, img)
        if os.path.exists(path):
            media.append(InputMediaPhoto(open(path, "rb")))

    if media:
        await update.message.reply_media_group(media)

    caption = (
        f"📌 {item['title']}\n"
        f"Effective Period:\n"
        f"{format_date(item['start'])} – {format_date(item['end'])}"
    )

    await update.message.reply_text(caption)


# ================= MESSAGE HANDLER =================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip() if update.message.text else ""
    user_id = update.effective_user.id

    # ===== BACK =====
    if msg == "⬅ Back":
        context.user_data.clear()
        await start(update, context)
        return

    # ===== ADMIN =====
    if msg == "👑 Admin":
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ No access")
            return
        await update.message.reply_text("Admin Menu:", reply_markup=get_admin_menu())
        return

    # ===== UPDATE CATEGORY =====
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

    mode = context.user_data.get("mode")

    # ===== SELECT NUMBER =====
    if mode == "select_number":
        context.user_data["item"] = msg
        context.user_data["mode"] = "image_a"
        await update.message.reply_text("Upload Gambar A")
        return

    # ===== IMAGE A =====
    if mode == "image_a":
        if update.message.photo:
            photo = update.message.photo[-1]
            file = await photo.get_file()

            folder = context.user_data["category"]
            item = context.user_data["item"]

            os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

            path = os.path.join(BASE_DIR, folder, f"{item}_a.jpg")
            await file.download_to_drive(path)

            context.user_data["mode"] = "image_b"
            await update.message.reply_text("Upload Gambar B")
        else:
            await update.message.reply_text("❌ Sila upload gambar.")
        return

    # ===== IMAGE B =====
    if mode == "image_b":
        if update.message.photo:
            photo = update.message.photo[-1]
            file = await photo.get_file()

            folder = context.user_data["category"]
            item = context.user_data["item"]

            path = os.path.join(BASE_DIR, folder, f"{item}_b.jpg")
            await file.download_to_drive(path)

            context.user_data["mode"] = "start_date"
            await update.message.reply_text("Masukkan tarikh START (YYYY-MM-DD)")
        else:
            await update.message.reply_text("❌ Sila upload gambar.")
        return

    # ===== START DATE =====
    if mode == "start_date":
        context.user_data["start"] = msg
        context.user_data["mode"] = "end_date"
        await update.message.reply_text("Masukkan tarikh END (YYYY-MM-DD)")
        return

    # ===== END DATE =====
    if mode == "end_date":
        data = load_data()

        category = context.user_data["category"]
        item = context.user_data["item"]

        data[category][item] = {
            "title": f"{category} {item}",
            "images": [
                f"{category}/{item}_a.jpg",
                f"{category}/{item}_b.jpg"
            ],
            "start": context.user_data["start"],
            "end": msg
        }

        save_data(data)

        context.user_data.clear()
        await update.message.reply_text("✅ Update berjaya")
        return

    # ===== VIEW OR =====
    if msg.startswith("OR "):
        key = msg.split(" ", 1)[1]
        await send_item(update, context, "OR", key)
        return

    # ===== VIEW GE =====
    if msg.startswith("GE "):
        key = msg.split(" ", 1)[1]
        await send_item(update, context, "GE", key)
        return

    # ===== MAIN MENU =====
    if msg == "📂 OR":
        await update.message.reply_text("Taip: OR 1, OR 2 dan sebagainya")
        return

    if msg == "📂 GE":
        await update.message.reply_text("Taip: GE 1, GE 2 dan sebagainya")
        return

    # ===== FALLBACK =====
    await update.message.reply_text(
        "Arahan tidak dikenali.",
        reply_markup=get_main_menu(user_id)
    )


# ================= MAIN =================

def main():
    print("===== DEBUG START =====")

    TOKEN = os.getenv("TOKEN")

    if not TOKEN:
        raise Exception("TOKEN NOT LOADED")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(~filters.COMMAND, handle_message))

    print("RUNNING POLLING...")
    app.run_polling()


if __name__ == "_main_":
    main()