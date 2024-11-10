from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes
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
#TOKEN = "7874734421:AAGeb_aIRqo_uoesUUJxjl0jrLZ9m3L6moc"

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
    await update.message.reply_animation(animation=GIF_OFF)


# Функция для отправки гифки при команде /kaban_on
async def kaban_on(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_animation(animation=GIF_ON)


# Функция для команды /day_X, которая рассчитывает время до 15 ноября 2024 года
async def day_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Текущее время
    now = datetime.now()
    # Разница между целевой датой и текущим временем
    time_left = TARGET_DATE - now

    # Проверяем, что дата не прошла
    if time_left.total_seconds() > 0:
        # Извлекаем дни, часы, минуты и секунды
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Формируем сообщение
        message = f"Времени до 15 ноября 2024 года:\n{days} дней, {hours} часов, {minutes} минут, {seconds} секунд"
    else:
        message = "15 ноября 2024 года уже наступило!"

    # Отправляем сообщение в чат
    await update.message.reply_text(message)


# Команда /good_coffee
async def good_coffee(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Текущее московское время
    now_msk = datetime.now(MSK_TZ)
    today_msk = now_msk.date()

    # Рассчитываем количество дней с начала "хорошей" смены
    days_since_good_shift_start = (today_msk - GOOD_SHIFT_START_DATE.date()).days

    # Если количество дней с начала смены делится на 4 с остатком 0 или 1, смена "хорошая"
    if days_since_good_shift_start % 4 < 2:
        await update.message.reply_animation(animation=GIF_COFFEE_GOOD)
    else:
        await update.message.reply_animation(animation=GIF_COFFEE_BAD)


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Перезапуск бота...")
    # restart_bot()

# Функция для команды /rabota
async def send_derevnja_durakov(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    # Выбоаудиофайла из папки (например, derevnja_durakov.mp3)
    file_path = os.path.join(
        SAMPLES_DIR, "derevnja_durakov.mp3"
    )  # Замените "derevnja_durakov.mp3" на нужный файл
    print(f"Путь к файлу: {file_path}")
    print(f"Файл существует: {os.path.exists(file_path)}")

    # Проверяем, существует ли файл
    if os.path.exists(file_path):
        # Отправляем аудиофайл
        await update.message.reply_audio(audio=open(file_path, "rb"))
    else:
        # Если файл не найден, отправляем сообщение об ошибке
        await update.message.reply_text("Аудиофайл не найден.")


# Функция для команды /z
async def send_z(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Выбор аудиофайла из папки (например, goida.mp3)
    file_path = os.path.join(
        SAMPLES_DIR, "goida.mp3"
    )  # Замените "goida.mp3" на нужный файл

    # Проверка, существует ли файл
    if os.path.exists(file_path):
        # Отправка аудиофайл
        await update.message.reply_audio(audio=open(file_path, "rb"))
    else:
        # Если файл не найден, отправляем сообщение об ошибке
        await update.message.reply_text("Аудиофайл не найден.")


# Функция для команды /casino
async def send_casino(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Выбираем аудиофайл из папки (например, casino.mp3)
    file_path = os.path.join(
        SAMPLES_DIR, "casino.mp3"
    )  # Замените "casino.mp3" на нужный файл

    # Проверяем, существует ли файл
    if os.path.exists(file_path):
        # Отправляем аудиофайл
        await update.message.reply_audio(audio=open(file_path, "rb"))
    else:
        # Если файл не найден, отправляем сообщение об ошибке
        await update.message.reply_text("Аудиофайл не найден.")


async def set_bot_commands(application: Application):
    await application.bot.set_my_commands(
        [
            BotCommand("kaban_off", "Природа очистилась"),
            BotCommand("kaban_on", "Природа загрязнилась"),
            BotCommand("day_x", "Отчёт времени до 15 ноября 2024 года"),
            BotCommand("good_coffee", "Проверить, хорошая ли смена готовит кофе"),
            BotCommand("vecherok", "Вечерок посидеть и готово"),
            BotCommand("rabota", "Чёрт-ти что"),
            BotCommand("z", "ГОЙДА"),
            BotCommand("casino", "Этого казино"),
        ]
    )


# Функция для команды /vecherok
async def vecherok(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_sticker(sticker=STICKER_VECHEROK)


def main():
    # Создания приложения для бота
    application = Application.builder().token(TOKEN).build()

    # Установка команд бота в момент инициализации
    application.post_init = set_bot_commands

    # Добавление обработчики команд
    application.add_handler(CommandHandler("kaban_off", kaban_off))
    application.add_handler(CommandHandler("kaban_on", kaban_on))
    application.add_handler(CommandHandler("day_x", day_x))
    application.add_handler(CommandHandler("good_coffee", good_coffee))
    application.add_handler(CommandHandler("restart", restart))
    application.add_handler(CommandHandler("vecherok", vecherok))
    application.add_handler(CommandHandler("rabota", send_derevnja_durakov))
    application.add_handler(CommandHandler("z", send_z))
    application.add_handler(CommandHandler("casino", send_casino))
    # Запуск бота
    application.run_polling()


# Проверка для запуска
if __name__ == "__main__":
    main()
