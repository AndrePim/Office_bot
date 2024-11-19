from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaAnimation, InputMediaAudio, Update, BotCommand
import telegram
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime, timedelta
import os
import sys
import asyncio
import pytz


# Московский часовой пояс
MSK_TZ = pytz.timezone("Europe/Moscow")
# def restart_bot():
#     os.execv(sys.executable, ["python"] + sys.argv)


# Токен вашего бота
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Ссылки на гифки
GIF_ON = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjl4OTZiaWd4YjNoMGRobGR1YXk3eTJxdmNvMTAxOXhtb3o3bDY1eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XE5z1TYI2w5RddJigU/giphy.gif"  # Первая гифка для команды /kaban_off
GIF_OFF = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2IybGdiMTlibjhzdjlyeHFubXpud2tuNDJmN2dhdTU5YjFzaXN3ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/NU9hqIw9vN0fm/giphy.gif"  # Вторая гифка для команды /kaban_on
GIF_COFFEE_GOOD = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3JrcGlqNHNqbzdja3hqcDlrOGlka2N0ZXFqM2JjOTZldzV5ZTUxcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/8cN6wDcWdzEGBsIRya/giphy-downsized-large.gif"
GIF_COFFEE_BAD = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2o3bXdweWhmbzNjbW5qdHY4YjU4b2tsYmJxMW9wN3c1bnh5a3IwMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Se7HIUfhVgXe0/giphy.gif"

STICKER_VECHEROK = "CAACAgIAAxkBAAENGklnMRdyvZhEBQtCXk7LywPpqGBrywACv2EAAp3aQEgCurLOJ4bKsTYE"

# Путь к папке с аудиофайлами
SAMPLES_DIR = "/app/samples"  # Убедитесь, что эта папка существует и содержит аудиофайлы

# Целевая дата
TARGET_DATE = datetime(2024, 11, 15)

# Первый день "хорошей" смены (например, 1 ноября 2024)
GOOD_SHIFT_START_DATE = datetime(2024, 11, 1)


# Функция для отправки гифки при команде /kaban_off
async def kaban_off(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.edit_message_media(
            media=InputMediaAnimation(GIF_OFF),
            reply_markup=None
        )
    elif update.message:
        await update.message.reply_animation(animation=GIF_OFF)

# Функция для отправки гифки при команде /kaban_on
async def kaban_on(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.edit_message_media(
            media=InputMediaAnimation(GIF_ON),
            reply_markup=None
        )
    elif update.message:
        await update.message.reply_animation(animation=GIF_ON)


def get_day_word_form(days: int) -> str:
    """Возвращает правильную форму слова 'день' в зависимости от числа."""
    if 11 <= days % 100 <= 19:  # Исключение для 11-19
        return "дней"
    last_digit = days % 10
    if last_digit == 1:
        return "день"
    elif 2 <= last_digit <= 4:
        return "дня"
    else:
        return "дней"

# Функция для команды /day_X, которая рассчитывает время до 15 ноября 2024 года
async def day_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    now = datetime.now()
    time_left = TARGET_DATE - now
    if time_left.total_seconds() > 0:
        days, seconds = time_left.days, time_left.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        day_word = get_day_word_form(days)
        message = f"До 15 ноября 2024 года:\n{days} {day_word}, {hours} часов, {minutes} минут, {seconds} секунд"
    else:
         # Расчет времени, прошедшего после 15 ноября 2024 года
        days_passed = (now - TARGET_DATE).days
        day_word = get_day_word_form(days_passed)
        message = f"15 ноября 2024 года уже наступило!\nПрошло {days_passed} {day_word}, а ещё никто не уволился."
    # Проверяем, откуда пришёл запрос, и отвечаем соответственно
    if update.callback_query:
        # Убираем кнопки и оставляем только текст
        await update.callback_query.edit_message_text(text=message)

# Команда /good_coffee
async def good_coffee(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    now_msk = datetime.now(MSK_TZ)
    days_since_start = (now_msk.date() - GOOD_SHIFT_START_DATE.date()).days
    animation = GIF_COFFEE_GOOD if days_since_start % 4 < 2 else GIF_COFFEE_BAD

    if update.callback_query:
        await update.callback_query.edit_message_media(
            media=InputMediaAnimation(animation),
            reply_markup=None
        )
    elif update.message:
        await update.message.reply_animation(animation=animation)

# 3. Аудио команды
async def send_derevnja_durakov(
    update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_audio(update, "derevnja_durakov.ogg")


async def send_z(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_audio(update, "goida.ogg")


async def send_casino(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_audio(update, "casino.ogg")


async def send_dimon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_audio(update, "dimon.ogg")


async def send_daladna(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_audio(update, "daladna.ogg")

async def send_audio(update: Update, file_name: str) -> None:
    file_path = os.path.join(SAMPLES_DIR, file_name)

    # Проверка существования файла
    if os.path.exists(file_path):
        # Убираем расширение .ogg из имени файла для заголовка
        file_name_without_extension = os.path.splitext(file_name)[0]
        caption = f"{file_name_without_extension}"

        # Попытка удаления предыдущего сообщения
        try:
            if update.message:
                await update.message.delete()
            elif update.callback_query:
                await update.callback_query.message.delete()
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")

        # Отправка нового сообщения с аудио
        try:
            if update.message:
                await update.message.reply_audio(audio=open(file_path, "rb"), caption=caption)
            elif update.callback_query:
                await update.callback_query.answer()  # Убираем "часики" в кнопке
                await update.callback_query.message.chat.send_audio(audio=open(file_path, "rb"), caption=caption)
        except Exception as e:
            print(f"Ошибка при отправке аудио: {e}")
    else:
        error_text = "Аудиофайл не найден."

        # Удаление предыдущего сообщения и отправка сообщения с ошибкой
        try:
            if update.message:
                await update.message.delete()
                await update.message.reply_text(error_text)
            elif update.callback_query:
                await update.callback_query.answer()  # Убираем "часики" в кнопке
                await update.callback_query.message.chat.send_message(error_text)
        except Exception as e:
            print(f"Ошибка при отправке сообщения с ошибкой: {e}")

# Меню категорий команд
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Время и смена", callback_data="time_menu")],
            [InlineKeyboardButton("Природа", callback_data="nature_menu")],
            [InlineKeyboardButton("Аудио команды", callback_data="audio_menu")],
        ]
    )

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text="Выберите категорию:", reply_markup=reply_markup
        )
    elif update.message:
        await update.message.reply_text(
            text="Выберите категорию:", reply_markup=reply_markup
        )


async def time_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    new_reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Время до 15 ноября", callback_data="day_x")],
            [
                InlineKeyboardButton(
                    "Проверить смену для кофе", callback_data="good_coffee"
                )
            ],
            [InlineKeyboardButton("Назад", callback_data="main_menu")],
        ]
    )

    # Обновляем текст сообщения и кнопки, если оно отличается
    try:
        await query.edit_message_text(
            text="Выберите категорию времени:", reply_markup=new_reply_markup
        )
    except telegram.error.BadRequest as e:
        if "Message is not modified" not in str(e):
            raise


async def nature_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Природа загрязнилась", callback_data="kaban_on")],
            [InlineKeyboardButton("Природа очистилась", callback_data="kaban_off")],
            [InlineKeyboardButton("Назад", callback_data="main_menu")],
        ]
    )

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text="Команды природы:", reply_markup=reply_markup
        )
    elif update.message:
        await update.message.reply_text(
            text="Команды природы:", reply_markup=reply_markup
        )


async def audio_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Деревня дураков", callback_data="rabota")],
            [InlineKeyboardButton("ГОЙДА", callback_data="z")],
            [InlineKeyboardButton("Казино", callback_data="casino")],
            [InlineKeyboardButton("Димон", callback_data="dimon")],
            [InlineKeyboardButton("Назад", callback_data="main_menu")],
        ]
    )

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text="Аудио команды:", reply_markup=reply_markup
        )
    elif update.message:
        await update.message.reply_text(
            text="Аудио команды:", reply_markup=reply_markup
        )

# Обработчик нажатий кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Удаление старых кнопок или сообщения
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except telegram.error.BadRequest as e:
        if "Message is not modified" not in str(e):
            raise

    if query.data == "main_menu":
        await menu(update, context)
    elif query.data == "time_menu":
        await time_menu(update, context)
    elif query.data == "nature_menu":
        await nature_menu(update, context)
    elif query.data == "audio_menu":
        await audio_menu(update, context)
    elif query.data == "day_x":
        await day_x(update, context)
    elif query.data == "good_coffee":
        await good_coffee(update, context)
    elif query.data == "kaban_on":
        await kaban_on(update, context)
    elif query.data == "kaban_off":
        await kaban_off(update, context)
    elif query.data == "rabota":
        await send_derevnja_durakov(update, context)
    elif query.data == "z":
        await send_z(update, context)
    elif query.data == "casino":
        await send_casino(update, context)
    elif query.data == "dimon":
        await send_dimon(update, context)
    elif query.data == "daladna":
        await send_daladna(update, context)

# Функция для команды /vecherok
async def vecherok(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_sticker(sticker=STICKER_VECHEROK)


def main():
    # Создания приложения для бота
    application = Application.builder().token(TOKEN).build()

    # Основное меню
    application.add_handler(CommandHandler("menu", menu))

    # Обработчик нажатий кнопок
    application.add_handler(CallbackQueryHandler(button_handler))

    # Запуск бота
    application.run_polling()


# Проверка для запуска
if __name__ == "__main__":
    main()
