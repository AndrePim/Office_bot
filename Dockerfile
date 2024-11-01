# Использование оф.образ Python
FROM python:3.11-slim

# Установка рабочей директории 
WORKDIR /app

# Копирование файла с кодом бота
COPY telegram_bot_kabanello.py .

# Установка зависимостей
RUN pip install python-telegram-bot

#Запуск бота
CMD ["python", "telegram_bot_kabanello.py"]