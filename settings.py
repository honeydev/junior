"""Модуль настроек проекта."""

import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


DATABASE_URL = os.getenv(
    'DATABASE_URL', 'postgres://junior:junior@127.0.0.1:5432/junior'
)
