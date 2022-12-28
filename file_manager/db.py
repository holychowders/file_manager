import sqlite3
from os import path
from sqlite3 import Cursor
from typing import List, Tuple, Union

DB_PATH = "test.db"


def init() -> None:
    if not path.exists(DB_PATH):
        init_new()


def init_new() -> None:
    cmd_create_files_table = "CREATE TABLE files(name TEXT NOT NULL, path TEXT NOT NULL)"
    cmd_insert_defaults_for_files = (
        "INSERT INTO files(name, path) VALUES ('sample_video', 'sample_video.mp4'), ('non_existent_video', 'video.dne')"
    )

    cmd_create_tags_table = (
        "CREATE TABLE tags(name TEXT NOT NULL, is_hidden BOOLEAN NOT NULL, is_selected BOOLEAN NOT NULL)"
    )
    cmd_insert_defaults_for_tags = (
        "INSERT INTO tags(name, is_hidden, is_selected) VALUES ('Favorite', 0, 0), ('Archive', 0, 0)"
    )

    db_commands = (
        cmd_create_files_table,
        cmd_create_tags_table,
        cmd_insert_defaults_for_files,
        cmd_insert_defaults_for_tags,
    )

    cursor = get_cursor()

    for cmd in db_commands:
        cursor.execute(cmd)

    cursor.connection.commit()


def fetch_tags() -> List[Tuple[Union[str, bool, bool]]]:
    cursor = get_cursor()
    return cursor.execute("SELECT * FROM tags").fetchall()


def fetch_files() -> List[Tuple[str]]:
    cursor = get_cursor()
    return cursor.execute("SELECT * FROM files").fetchall()


def get_cursor() -> Cursor:
    return sqlite3.connect(DB_PATH).cursor()


def disable_tag_visibility(tag: str) -> None:
    get_cursor().execute(f"UPDATE tags SET is_hidden=1 WHERE name='{tag}'").connection.commit()


def enable_tag_visibility(tag: str) -> None:
    get_cursor().execute(f"UPDATE tags SET is_hidden=0 WHERE name='{tag}'").connection.commit()


def create_tag(tag: str) -> None:
    get_cursor().execute(f"INSERT INTO tags(name, is_hidden, is_selected) VALUES ('{tag}', 0, 0)").connection.commit()


def disable_tag_selection(tag: str) -> None:
    get_cursor().execute(f"UPDATE tags SET is_selected=0 WHERE name='{tag}'").connection.commit()
