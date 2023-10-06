# Используйте образ Python 3.8 или другой подходящий
FROM python:3.8

# Создайте директорию для приложения внутри контейнера
RUN mkdir /app

# Копируем requirements.txt в контейнер
COPY requirements.txt /app/

WORKDIR /app

# Устанавливаем зависимости из requirements.txt
RUN pip install -r requirements.txt

COPY . /app

# Команда для запуска бота
CMD ["python", "bot.py"]