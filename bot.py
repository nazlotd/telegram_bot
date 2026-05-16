import json
import os
from datetime import datetime, timedelta, timezone
from json import JSONDecodeError
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from telegram import InputMediaPhoto, ReplyKeyboardMarkup, Update
from telegram.error import TelegramError
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from config import (
    ADMIN_ID,
    BUTTON_ADMIN,
    BUTTON_BACK,
    BUTTON_DATE_INFO,
    BUTTON_GE,
    BUTTON_OR,
    CATEGORIES,
    CATEGORY_4_RM10,
    CATEGORY_GE,
    CATEGORY_OR,
    CATEGORY_STANDEE,
    DATA_DIR,
    DATA_FILE,
    INTRO_FILE,
    TOKEN,
    USERS_FILE,
)


def default_data():
    return {category: {} for category in CATEGORIES}


def load_data():
    if not os.path.exists(DATA_FILE):
        return default_data()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (JSONDecodeError, OSError):
        return default_data()

    if not isinstance(data, dict):
        return default_data()

    for category in CATEGORIES:
        if not isinstance(data.get(category), dict):
            data[category] = {}

    return data


def save_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            users = json.load(file)
    except (JSONDecodeError, OSError):
        return {}

    if not isinstance(users, dict):
        return {}

    return users


def save_users(users):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)


def malaysia_now():
    try:
        return datetime.now(ZoneInfo("Asia/Kuala_Lumpur"))
    except ZoneInfoNotFoundError:
        return datetime.now(timezone(timedelta(hours=8)))


def save_user(update):
    user = update.effective_user
    chat = update.effective_chat

    if not user:
        return

    users = load_users()
    user_id = str(user.id)
    now = malaysia_now().strftime("%d/%m/%Y %H:%M:%S")
    old_user = users.get(user_id, {})

    users[user_id] = {
        "id": user.id,
        "chat_id": chat.id if chat else None,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "language_code": user.language_code,
        "is_bot": user.is_bot,
        "is_admin": user.id == ADMIN_ID,
        "first_seen": old_user.get("first_seen", now),
        "last_seen": now,
        "message_count": old_user.get("message_count", 0) + 1,
    }

    save_users(users)


def get_main_menu(user_id):
    buttons = [
        [BUTTON_OR, BUTTON_GE],
        [CATEGORY_4_RM10, CATEGORY_STANDEE],
        [BUTTON_DATE_INFO],
    ]

    if user_id == ADMIN_ID:
        buttons.append([BUTTON_ADMIN])

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def get_back_menu():
    return ReplyKeyboardMarkup([[BUTTON_BACK]], resize_keyboard=True)


def get_admin_menu():
    return ReplyKeyboardMarkup(
        [
            ["UPDATE OR", "UPDATE GE"],
            ["UPDATE 4 RM10", "UPDATE STANDEE"],
            ["ADMIN STATS", "USER LIST"],
            ["PROMO LIST", "STORAGE INFO"],
            [BUTTON_BACK],
        ],
        resize_keyboard=True,
    )


def normalise_back_button(message):
    return message.endswith(BUTTON_BACK)


def is_admin_button(message):
    return message == BUTTON_ADMIN or message.endswith("Admin")


def is_or_button(message):
    return message in {BUTTON_OR, "📁 OR"} or message.endswith(" OR")


def is_ge_button(message):
    return message in {BUTTON_GE, "📁 GE"} or message.endswith(" GE")


def is_valid_date(message):
    try:
        datetime.strptime(message, "%d/%m/%Y")
    except ValueError:
        return False
    return True


def parse_seen_time(value):
    try:
        return datetime.strptime(value, "%d/%m/%Y %H:%M:%S")
    except (TypeError, ValueError):
        return datetime.min


def get_user_display_name(user):
    name_parts = [
        user.get("first_name") or "",
        user.get("last_name") or "",
    ]
    full_name = " ".join(part for part in name_parts if part).strip()
    username = user.get("username")

    if username:
        return f"@{username}"

    if full_name:
        return full_name

    return str(user.get("id", "Unknown"))


def build_caption(item):
    return (
        "╭━━━【 PROMOTION 】━━━╮\n\n"
        f"Title: {item.get('title', '')}\n\n"
        "Effective Date\n"
        f"{item.get('start', '')} -> {item.get('end', '')}\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "Please refer to Nazs for latest update."
    )


def get_photo_file_id(update):
    if not update.message or not update.message.photo:
        return None
    return update.message.photo[-1].file_id


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    save_user(update)

    if os.path.exists(INTRO_FILE):
        with open(INTRO_FILE, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption="Welcome. Sila pilih kategori di bawah.",
            )
    else:
        await update.message.reply_text(
            "Welcome to OR & GE Bot.\n\nSila pilih kategori di bawah."
        )

    await show_main_menu(update, context)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    save_user(update)
    await show_main_menu(update, context)


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    save_user(update)

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("No access.")
        return

    context.user_data.clear()
    await show_admin_menu(update, context)


async def show_or_menu(update, context):
    data = load_data()
    buttons = [[f"OR {key}"] for key in sorted(data[CATEGORY_OR].keys(), key=str)]
    buttons.append([BUTTON_BACK])

    await update.message.reply_text(
        "OR LIST",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
    )


async def show_ge_menu(update, context):
    data = load_data()
    buttons = [[f"GE {key}"] for key in sorted(data[CATEGORY_GE].keys(), key=str)]
    buttons.append([BUTTON_BACK])

    await update.message.reply_text(
        "GE LIST",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
    )


async def show_standee_menu(update, context):
    data = load_data()
    standee_data = data.get(CATEGORY_STANDEE, {})
    buttons = [[key] for key in sorted(standee_data.keys(), key=str)]
    buttons.append([BUTTON_BACK])

    await update.message.reply_text(
        "Pilih Standee:",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
    )


async def show_admin_menu(update, context):
    await update.message.reply_text(
        "Admin Panel",
        reply_markup=get_admin_menu(),
    )


async def show_main_menu(update, context):
    context.user_data.clear()
    await update.message.reply_text(
        "Main Menu:",
        reply_markup=get_main_menu(update.effective_user.id),
    )


async def send_images(update, context, item):
    if not update.message:
        return

    images = item.get("images", [])
    if not isinstance(images, list):
        images = []

    images = [image for image in images if image]

    if not images:
        await update.message.reply_text("Tiada gambar.")
        return

    caption = build_caption(item)

    try:
        if len(images) == 1:
            await update.message.reply_photo(photo=images[0], caption=caption)
            return

        media = [
            InputMediaPhoto(media=file_id, caption=caption if index == 0 else None)
            for index, file_id in enumerate(images)
        ]
        await context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=media,
        )
    except TelegramError as error:
        await update.message.reply_text(
            f"Gagal hantar gambar. Sila update gambar semula.\nError: {error}"
        )


async def show_admin_stats(update):
    data = load_data()
    users = load_users()
    category_lines = []

    for category in CATEGORIES:
        items = data.get(category, {})
        total_items = len(items)
        total_images = sum(
            len(item.get("images", []))
            for item in items.values()
            if isinstance(item, dict) and isinstance(item.get("images", []), list)
        )
        category_lines.append(f"{category}: {total_items} item, {total_images} gambar")

    response = (
        "ADMIN STATS\n"
        "------------------\n"
        f"Total user: {len(users)}\n\n"
        "Promo:\n"
        + "\n".join(category_lines)
    )

    await update.message.reply_text(response, reply_markup=get_admin_menu())


async def show_user_list(update, limit=15):
    users = load_users()

    if not users:
        await update.message.reply_text(
            "Belum ada user disimpan.",
            reply_markup=get_admin_menu(),
        )
        return

    sorted_users = sorted(
        users.values(),
        key=lambda user: parse_seen_time(user.get("last_seen")),
        reverse=True,
    )

    lines = [f"USER LIST ({len(users)} total)", "------------------"]
    for index, user in enumerate(sorted_users[:limit], start=1):
        lines.append(
            f"{index}. {get_user_display_name(user)} | ID: {user.get('id')} | "
            f"Msg: {user.get('message_count', 0)} | Last: {user.get('last_seen', '-')}"
        )

    if len(users) > limit:
        lines.append(f"\nPaparan {limit} user terbaru sahaja.")

    await update.message.reply_text("\n".join(lines), reply_markup=get_admin_menu())


async def show_promo_list(update):
    data = load_data()
    lines = ["PROMO LIST", "------------------"]

    for category in CATEGORIES:
        items = data.get(category, {})
        if not items:
            lines.append(f"{category}: kosong")
            continue

        item_keys = ", ".join(sorted(items.keys(), key=str))
        lines.append(f"{category}: {item_keys}")

    await update.message.reply_text("\n".join(lines), reply_markup=get_admin_menu())


async def show_storage_info(update):
    data = load_data()
    users = load_users()
    data_exists = os.path.exists(DATA_FILE)
    users_exists = os.path.exists(USERS_FILE)
    data_size = os.path.getsize(DATA_FILE) if data_exists else 0
    users_size = os.path.getsize(USERS_FILE) if users_exists else 0

    promo_count = sum(len(data.get(category, {})) for category in CATEGORIES)

    response = (
        "STORAGE INFO\n"
        "------------------\n"
        f"DATA_DIR:\n{DATA_DIR}\n\n"
        f"DATA_FILE:\n{DATA_FILE}\n"
        f"Exists: {data_exists}\n"
        f"Size: {data_size} bytes\n\n"
        f"USERS_FILE:\n{USERS_FILE}\n"
        f"Exists: {users_exists}\n"
        f"Size: {users_size} bytes\n\n"
        f"Promo item: {promo_count}\n"
        f"User: {len(users)}"
    )

    await update.message.reply_text(response, reply_markup=get_admin_menu())


async def handle_admin_panel_action(update, message):
    if message == "ADMIN STATS":
        await show_admin_stats(update)
        return True

    if message == "USER LIST":
        await show_user_list(update)
        return True

    if message == "PROMO LIST":
        await show_promo_list(update)
        return True

    if message == "STORAGE INFO":
        await show_storage_info(update)
        return True

    return False


async def ask_for_update_number(update, context, category):
    context.user_data.clear()
    context.user_data["category"] = category
    context.user_data["mode"] = "select_number"
    await update.message.reply_text(
        f"{category} nombor berapa?",
        reply_markup=get_back_menu(),
    )


async def handle_update_trigger(update, context, message):
    if message == "UPDATE OR":
        await ask_for_update_number(update, context, CATEGORY_OR)
        return True

    if message == "UPDATE GE":
        await ask_for_update_number(update, context, CATEGORY_GE)
        return True

    if message == "UPDATE STANDEE":
        await ask_for_update_number(update, context, CATEGORY_STANDEE)
        return True

    if message == "UPDATE 4 RM10":
        context.user_data.clear()
        context.user_data["category"] = CATEGORY_4_RM10
        context.user_data["item"] = "1"
        context.user_data["mode"] = "image_a"
        await update.message.reply_text(
            "Upload gambar baru.",
            reply_markup=get_back_menu(),
        )
        return True

    return False


async def handle_admin_state(update, context, message):
    mode = context.user_data.get("mode")
    if not mode:
        return False

    if mode == "select_number":
        if not message.isdigit():
            await update.message.reply_text("Sila masukkan nombor yang sah.")
            return True

        context.user_data["item"] = message
        context.user_data["mode"] = "image_a"
        await update.message.reply_text("Upload Gambar A.")
        return True

    if mode == "image_a":
        file_id = get_photo_file_id(update)
        if not file_id:
            await update.message.reply_text("Sila upload gambar, bukan teks.")
            return True

        folder = context.user_data["category"]
        item_key = context.user_data["item"]

        data = load_data()
        data.setdefault(folder, {})
        data[folder].setdefault(item_key, {})
        data[folder][item_key]["images"] = [file_id]
        save_data(data)

        if folder == CATEGORY_4_RM10:
            context.user_data["mode"] = "start_date"
            await update.message.reply_text("Masukkan tarikh mula (DD/MM/YYYY).")
        else:
            context.user_data["mode"] = "image_b"
            await update.message.reply_text("Upload Gambar B.")
        return True

    if mode == "image_b":
        file_id = get_photo_file_id(update)
        if not file_id:
            await update.message.reply_text("Sila upload gambar, bukan teks.")
            return True

        folder = context.user_data["category"]
        item_key = context.user_data["item"]

        data = load_data()
        data.setdefault(folder, {})
        data[folder].setdefault(item_key, {})
        data[folder][item_key].setdefault("images", [])
        data[folder][item_key]["images"].append(file_id)
        save_data(data)

        context.user_data["mode"] = "start_date"
        await update.message.reply_text("Masukkan tarikh mula (DD/MM/YYYY).")
        return True

    if mode == "start_date":
        if not is_valid_date(message):
            await update.message.reply_text("Masukkan tarikh mula (DD/MM/YYYY).")
            return True

        context.user_data["start_date"] = message
        context.user_data["mode"] = "end_date"
        await update.message.reply_text("Masukkan tarikh tamat (DD/MM/YYYY).")
        return True

    if mode == "end_date":
        if not is_valid_date(message):
            await update.message.reply_text("Masukkan tarikh tamat (DD/MM/YYYY).")
            return True

        folder = context.user_data["category"]
        item_key = context.user_data["item"]

        data = load_data()
        data.setdefault(folder, {})
        data[folder].setdefault(item_key, {})
        data[folder][item_key]["title"] = (
            CATEGORY_4_RM10 if folder == CATEGORY_4_RM10 else f"{folder} {item_key}"
        )
        data[folder][item_key]["start"] = context.user_data["start_date"]
        data[folder][item_key]["end"] = message
        save_data(data)

        context.user_data.clear()
        await update.message.reply_text("Update berjaya!")
        await show_main_menu(update, context)
        return True

    context.user_data.clear()
    await update.message.reply_text("Sesi update tidak sah. Sila mula semula.")
    await show_main_menu(update, context)
    return True


async def handle_date_info(update):
    now = malaysia_now()
    date_45 = now + timedelta(days=45)
    date_60 = now + timedelta(days=60)
    date_90 = now + timedelta(days=90)

    response = (
        "DATE INFO\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"45 Days -> {date_45.strftime('%d/%m/%Y')}\n"
        f"60 Days -> {date_60.strftime('%d/%m/%Y')}\n"
        f"90 Days -> {date_90.strftime('%d/%m/%Y')}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Generated: {now.strftime('%d/%m/%Y %H:%M')}\n"
        "TIME WAITS FOR NO ONE"
    )

    await update.message.reply_text(response)


# ================= MESSAGE HANDLER =================
async def handle_message(update, context):
    if not update.message:
        return

    save_user(update)

    message = update.message.text.strip() if update.message.text else ""
    user_id = update.effective_user.id

    if normalise_back_button(message):
        await show_main_menu(update, context)
        return

    if is_admin_button(message):
        if user_id != ADMIN_ID:
            await update.message.reply_text("No access.")
            return

        context.user_data.clear()
        await show_admin_menu(update, context)
        return

    if user_id == ADMIN_ID and await handle_admin_panel_action(update, message):
        return

    if user_id == ADMIN_ID and await handle_update_trigger(update, context, message):
        return

    if await handle_admin_state(update, context, message):
        return

    data = load_data()

    if is_or_button(message):
        await show_or_menu(update, context)
        return

    if is_ge_button(message):
        await show_ge_menu(update, context)
        return

    if message == CATEGORY_4_RM10:
        item = data.get(CATEGORY_4_RM10, {}).get("1")
        if item:
            await send_images(update, context, item)
        else:
            await update.message.reply_text("Promo belum diset.")
        return

    if message == CATEGORY_STANDEE:
        await show_standee_menu(update, context)
        return

    standee_data = data.get(CATEGORY_STANDEE, {})
    if message in standee_data:
        await send_images(update, context, standee_data[message])
        return

    if message.startswith("OR "):
        key = message.split(" ", 1)[1].strip()
        item = data.get(CATEGORY_OR, {}).get(key)
        if item:
            await send_images(update, context, item)
        else:
            await update.message.reply_text("OR tidak wujud.")
        return

    if message.startswith("GE "):
        key = message.split(" ", 1)[1].strip()
        item = data.get(CATEGORY_GE, {}).get(key)
        if item:
            await send_images(update, context, item)
        else:
            await update.message.reply_text("GE tidak wujud.")
        return

    if message == BUTTON_DATE_INFO:
        await handle_date_info(update)
        return

    await update.message.reply_text(
        "Arahan tidak dikenali.\nSila pilih menu.",
        reply_markup=get_main_menu(user_id),
    )


# ================= MAIN =================
def main():
    if not TOKEN:
        raise RuntimeError("TOKEN tidak dijumpai. Set environment variable TOKEN dulu.")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(MessageHandler(~filters.COMMAND, handle_message))

    print("Bot running...")
    print(f"DATA_DIR: {DATA_DIR}")
    print(f"DATA_FILE: {DATA_FILE}")
    print(f"USERS_FILE: {USERS_FILE}")
    app.run_polling()


if __name__ == "__main__":
    main()
