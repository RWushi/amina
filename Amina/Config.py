import os
import json
import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()


API_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

app = web.Application()


DATABASE_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASS"),
    'port': os.getenv("DB_PORT")
}


class DB:
    async def __aenter__(self):
        self.conn = await asyncpg.connect(**DATABASE_CONFIG)
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()


def load_translations(path='translations'):
    translations = {}
    for lang_file in os.listdir(path):
        lang_code = lang_file.split('.')[0]
        with open(os.path.join(path, lang_file), 'r', encoding='utf-8') as f:
            translations[lang_code] = json.load(f)
    return translations


TRANSLATIONS = load_translations()


async def get_translation(language_code, category, key):
    return TRANSLATIONS[language_code][category][key]


USER_LANGUAGES = {}


async def set_language(user_id, language_code):
    USER_LANGUAGES[user_id] = language_code


async def get_language(user_id):
    return USER_LANGUAGES[user_id]


class States(StatesGroup):
    languages = State()
    menu = State()
    about = State()
    day = State()
    meeting = State()
    secret = State()
    rate = State()
    rwushi = State()

messages_ids = {}
