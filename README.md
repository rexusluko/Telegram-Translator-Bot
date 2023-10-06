# Первоначальные настройки
1. Зарегестрировать бота с помощью @BotFather (https://t.me/BotFather)  и получить токен
2. (Опционально) Заргестрироваться в Deepl (https://www.deepl.com/ru/pro-api?cta=header-pro-api) и получить ключ
3. Создать .env файл в корневой директории проекта с содержимым
```
DATABASE=example_db
USER=example_user
PASSWORD=example_password
TOKEN = example_token
DEEPL_API_KEY = example_key
ADMIN_ID = example_id
```
Данные из примера нужно заменить на свои
# Запуск приложения
С помощью консоли перейти в корневую директорию и выполнить
```
docker-compose up
```
# Работа с приложением
1. Для начала работы написать боту
```
/start
```
2. Для перехода в режим администратора написать
```
/admin
```