"""Модуль настроек проекта."""

from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())


DATABASE_URL = os.getenv(
    'DATABASE_URL', 'postgres://junior:junior@127.0.0.1:5432/junior'
)
