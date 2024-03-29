import json
import os
import sqlite3
from dataclasses import dataclass
from sqlite3 import Cursor
from tkinter import IntVar

_DB_PATH = "test.db"


@dataclass
class Tag:
    name: str
    is_hidden: bool
    is_selected: IntVar


@dataclass
class DisplayInfo:
    title: str
    info: str


@dataclass
class File:
    name: str
    path: str
    tags: list[str]

    def get_display_info(self) -> tuple[DisplayInfo, ...]:
        tags_info = ""
        for tag in self.tags:
            tags_info += f"{tag}, " if tag != self.tags[-1] else tag
        return DisplayInfo("Name", self.name), DisplayInfo("Path", self.path), DisplayInfo("Tags", tags_info)


def init() -> None:
    if not os.path.exists(_DB_PATH):  # noqa: PTH110
        _create_new()


def debug() -> None:
    print("\nDB DEBUG:")
    print("files:\n", _fetch_files())
    print("\ntags:\n", _fetch_tags())


def fetch_files() -> list[File]:
    files = _fetch_files()
    file_results = []

    for name, path, tags in files:
        file_results.append(File(name, path, json.loads(tags)))

    return file_results


# TAGS


def fetch_tags() -> list[Tag]:
    tags = _fetch_tags()
    content_tags = []

    for tag, is_hidden, is_selected_in_db in tags:
        is_selected = IntVar()
        is_selected.set(is_selected_in_db)

        content_tags.append(Tag(name=tag, is_hidden=is_hidden, is_selected=is_selected))

    return content_tags


def create_tag(tag: str) -> None:
    sql = f"INSERT INTO tags(name, is_hidden, is_selected) VALUES ('{tag}', 0, 0)"  # noqa: S608
    _get_cursor().execute(sql).connection.commit()


def disable_tag_visibility(tag: str) -> None:
    _get_cursor().execute(f"UPDATE tags SET is_hidden=1 WHERE name='{tag}'").connection.commit()  # noqa: S608


def enable_tag_visibility(tag: str) -> None:
    _get_cursor().execute(f"UPDATE tags SET is_hidden=0 WHERE name='{tag}'").connection.commit()  # noqa: S608


def toggle_tag_selection(tag: Tag) -> None:
    _get_cursor().execute(
        f"UPDATE tags SET is_selected={tag.is_selected.get()} WHERE name='{tag.name}'",  # noqa: S608
    ).connection.commit()


def disable_tag_selection(tag: str) -> None:
    _get_cursor().execute(f"UPDATE tags SET is_selected=0 WHERE name='{tag}'").connection.commit()  # noqa: S608


def clear_all_tag_selections() -> None:
    _get_cursor().execute("UPDATE tags SET is_selected=0 ").connection.commit()


# PRIVATES


def _create_new() -> None:
    db_commands = (
        "CREATE TABLE files(name TEXT NOT NULL, path TEXT NOT NULL, tags JSON_DUMPS NOT NULL)",
        "CREATE TABLE tags(name TEXT NOT NULL, is_hidden BOOLEAN NOT NULL, is_selected BOOLEAN NOT NULL)",
        f"""
        INSERT INTO files(name, path, tags)
        VALUES
        (
            'somewhat_really_long_sample_video_name',
            'somewhat_really_long_sample_video_name.mp4',
            '{json.dumps(('Favorite', 'Archive'))}'),
        (
            'non_existent_video',
            'video.dne',
            '{json.dumps(('Archive',))}'
        )
        """,
        "INSERT INTO tags(name, is_hidden, is_selected) VALUES ('Favorite', 0, 0), ('Archive', 0, 0)",
    )

    cursor = _get_cursor()

    for cmd in db_commands:
        cursor.execute(cmd)

    cursor.connection.commit()


def _fetch_tags() -> list[tuple[str, bool, bool]]:
    return _get_cursor().execute("SELECT * FROM tags").fetchall()


def _fetch_files() -> list[tuple[str, str, str]]:
    return _get_cursor().execute("SELECT * FROM files").fetchall()


def _get_cursor() -> Cursor:
    return sqlite3.connect(_DB_PATH).cursor()
