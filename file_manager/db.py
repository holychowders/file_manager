import sqlite3
from os import path
from sqlite3 import Cursor
from typing import List, Tuple

DB_PATH = "test.db"


def init_db() -> None:
    if not path.exists(DB_PATH):
        init_new_db()


def init_new_db() -> None:
    cmd_create_files_table = "CREATE TABLE files(name TEXT NOT NULL, path TEXT NOT NULL)"
    cmd_create_tags_table = "CREATE TABLE tags(name TEXT NOT NULL)"
    cmd_insert_defaults_for_tags = "INSERT INTO tags(name) VALUES('Favorite')"

    db_commands = cmd_create_files_table, cmd_create_tags_table, cmd_insert_defaults_for_tags

    cursor = get_db_cursor()

    for cmd in db_commands:
        cursor.execute(cmd)

    cursor.connection.commit()


def fetch_tags_from_db() -> List[str]:
    cursor = get_db_cursor()
    return cursor.execute("SELECT * FROM tags").fetchall()


def fetch_files_from_db() -> List[Tuple[str]]:
    cursor = get_db_cursor()
    return cursor.execute("SELECT * FROM files").fetchall()


def get_db_cursor() -> Cursor:
    return sqlite3.connect(DB_PATH).cursor()
