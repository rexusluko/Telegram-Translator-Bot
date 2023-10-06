import asyncpg
from decouple import config

DATABASE = config('DATABASE')
USER = config('USER')
PASSWORD = config('PASSWORD')
HOST = 'postgres'

async def create_users_table():
    con = await asyncpg.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST)
    create_users_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY
    );
    """
    await con.execute(create_users_table_query)
    await con.close()


async def create_translations_table():
    con = await asyncpg.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST)
    create_translations_table_query = """
    CREATE TABLE IF NOT EXISTS translations (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
        time TIMESTAMP DEFAULT NOW(),
        original_text TEXT NOT NULL,
        result TEXT NOT NULL
    );
    """
    await con.execute(create_translations_table_query)
    await con.close()


async def add_user(user_id: int):
    con = await asyncpg.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST)
    insert_user_query = f"INSERT INTO users (user_id) VALUES ({user_id}) ON CONFLICT (user_id) DO NOTHING;"
    await con.execute(insert_user_query)
    await con.close()


async def add_translation(user_id: int, text_to_translate: str, translated_text: str):
    con = await asyncpg.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST)
    insert_translation_query = f"INSERT INTO translations (user_id, original_text, result) VALUES ({user_id}, " \
                               f"'{text_to_translate}', '{translated_text}');"
    await con.execute(insert_translation_query)
    await con.close()


async def get_translations_by_user(user_id: int):
    con = await asyncpg.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST)
    get_translations_query = f"SELECT * FROM translations WHERE user_id = {user_id};"
    translations = await con.fetch(get_translations_query)
    await con.close()

    # Форматируем результаты в виде текстовой таблицы
    if translations:
        table = ""
        for row in translations:
            # Используем табуляцию для разделения значений
            original_text = row['original_text']
            translated_text = row['result']
            time = row['time']
            formatted_row = f"{original_text} → {translated_text} ({time})"
            table += formatted_row + "\n"
        return table
    else:
        return "Нет записей для данного пользователя."


async def get_all_translations():
    con = await asyncpg.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST)
    get_translations_query = "SELECT * FROM translations;"
    translations = await con.fetch(get_translations_query)
    await con.close()

    # Форматируем результаты в виде текстовой таблицы
    if translations:
        table = ""
        for row in translations:
            user_id = row['user_id']
            original_text = row['original_text']
            translated_text = row['result']
            time = row['time']
            formatted_row = f"{user_id} {original_text} → {translated_text} ({time})"
            table += formatted_row + "\n"
        return table
    else:
        return "Нет записей в таблице translations."
