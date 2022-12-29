import os
import sqlite3
from dataclasses import dataclass
from sqlite3 import Cursor
from tkinter import IntVar
from typing import List, Tuple

_DB_PATH = "test.db"


@dataclass
class Tag:
    name: str
    is_hidden: bool
    is_selected: IntVar


@dataclass
class File:
    name: str
    path: str


def init() -> None:
    if not os.path.exists(_DB_PATH):
        _create_new()


def debug() -> None:
    print("\nDB DEBUG:")
    print("files:\n", _fetch_files())
    print("\ntags:\n", _fetch_tags())


def fetch_files() -> List[File]:
    files = _fetch_files()
    file_results = []

    for name, path in files:
        file_results.append(File(name, path))

    return file_results


# TAGS


def fetch_tags() -> List[Tag]:
    tags = _fetch_tags()
    content_tags = []

    for tag, is_hidden, is_selected_in_db in tags:
        is_selected = IntVar()
        is_selected.set(is_selected_in_db)

        content_tags.append(Tag(name=tag, is_hidden=is_hidden, is_selected=is_selected))

    return content_tags


def create_tag(tag: str) -> None:
    _get_cursor().execute(f"INSERT INTO tags(name, is_hidden, is_selected) VALUES ('{tag}', 0, 0)").connection.commit()


def disable_tag_visibility(tag: str) -> None:
    _get_cursor().execute(f"UPDATE tags SET is_hidden=1 WHERE name='{tag}'").connection.commit()


def enable_tag_visibility(tag: str) -> None:
    _get_cursor().execute(f"UPDATE tags SET is_hidden=0 WHERE name='{tag}'").connection.commit()


def toggle_tag_selection(tag: Tag) -> None:
    _get_cursor().execute(
        f"UPDATE tags SET is_selected={tag.is_selected.get()} WHERE name='{tag.name}'"
    ).connection.commit()


def disable_tag_selection(tag: str) -> None:
    _get_cursor().execute(f"UPDATE tags SET is_selected=0 WHERE name='{tag}'").connection.commit()


def clear_all_tag_selections() -> None:
    _get_cursor().execute("UPDATE tags SET is_selected=0 ").connection.commit()


# PRIVATES


def _create_new() -> None:
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

    cursor = _get_cursor()

    for cmd in db_commands:
        cursor.execute(cmd)

    cursor.connection.commit()


def _fetch_tags() -> List[Tuple[str, bool, bool]]:
    return _get_cursor().execute("SELECT * FROM tags").fetchall()


def _fetch_files() -> List[Tuple[str, str]]:
    return _get_cursor().execute("SELECT * FROM files").fetchall()


def _get_cursor() -> Cursor:
    return sqlite3.connect(_DB_PATH).cursor()
