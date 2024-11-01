from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, timedelta
import os
import sys


def restart_bot():
    os.execv(sys.executable, ["python"] + sys.argv)


# Токен вашего бота
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Ссылки на гифки
GIF_ON = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjl4OTZiaWd4YjNoMGRobGR1YXk3eTJxdmNvMTAxOXhtb3o3bDY1eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XE5z1TYI2w5RddJigU/giphy.gif"  # Первая гифка для команды /kaban_off
GIF_OFF = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2IybGdiMTlibjhzdjlyeHFubXpud2tuNDJmN2dhdTU5YjFzaXN3ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/NU9hqIw9vN0fm/giphy.gif"  # Вторая гифка для команды /kaban_on

# Целевая дата
TARGET_DATE = datetime(2024, 11, 15)


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


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Перезапуск бота...")
    restart_bot()


# Основная функция для запуска бота
def main():
    # Создаем приложение для бота
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("kaban_off", kaban_off))
    application.add_handler(CommandHandler("kaban_on", kaban_on))
    application.add_handler(CommandHandler("day_x", day_x))
    application.add_handler(CommandHandler("restart", restart))

    # Устанавливаем команды для отображения при вводе '/'
    application.bot.set_my_commands(
        [
            BotCommand("kaban_off", "Природа очистилась"),
            BotCommand("kaban_on", "Природа загрязнилась"),
            BotCommand("day_x", "Отчёт времени до 15 ноября 2024 года"),
        ]
    )

    # Запускаем бота
    application.run_polling()


if __name__ == "__main__":
    main()