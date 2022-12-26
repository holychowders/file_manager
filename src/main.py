import sqlite3
from dataclasses import dataclass
from os import path
from sqlite3 import Cursor
from tkinter import Button, Checkbutton, IntVar, Label, Tk
from typing import List, Tuple

DB_PATH = "test.db"


def main(debug: bool) -> None:
    init_db()

    GUI(debug).run()


def init_db():
    if not path.exists(DB_PATH):
        init_new_db()


def init_new_db():
    cmd_create_files_table = "CREATE TABLE files(name TEXT NOT NULL, path TEXT NOT NULL)"
    cmd_create_tags_table = "CREATE TABLE tags(name TEXT NOT NULL)"
    cmd_insert_defaults_for_tags = "INSERT INTO tags(name) VALUES('Favorite')"

    db_commands = cmd_create_files_table, cmd_create_tags_table, cmd_insert_defaults_for_tags

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for cmd in db_commands:
        cursor.execute(cmd)

    connection.commit()


def fetch_tags_from_db() -> List[str]:
    cursor = get_db_cursor()
    return cursor.execute("SELECT * FROM tags").fetchall()


def fetch_files_from_db() -> List[Tuple[str]]:
    cursor = get_db_cursor()
    return cursor.execute("SELECT * FROM files").fetchall()


def get_db_cursor() -> Cursor:
    return sqlite3.connect(DB_PATH).cursor()


class GUI:
    def __init__(self, debug=False):
        gui = Tk()
        gui.title("File Manager")
        gui.iconbitmap("assets/main-icon-512px-colored.ico")
        gui.geometry("400x600")

        self.gui = gui

        if debug:
            self.debug()

        self.init_content_tags()

    def run(self) -> None:
        self.gui.mainloop()

    # Tags stuff

    def init_content_tags(self) -> None:
        self.tags: List[ContentTag] = []
        self.fetch_tags_from_db()
        self.add_tags_selection()

    def add_tags_selection(self):
        Label(self.gui, text="Tags").pack()

        for tag in self.tags:
            Checkbutton(self.gui, text=tag.name, variable=tag.is_selected).pack()

    def fetch_tags_from_db(self) -> None:
        tags = fetch_tags_from_db()

        for tag in tags:
            self.tags.append(ContentTag(tag, IntVar()))

    # Debugging stuff

    def debug(self) -> None:
        self.add_debug_button()

    def add_debug_button(self) -> None:
        Button(self.gui, text="Debug", command=self.debug_db).pack()

    @staticmethod
    def debug_db() -> None:
        print("\nDB DEBUG:")
        print("files:\n", fetch_files_from_db())
        print("\ntags:\n", fetch_tags_from_db())


@dataclass
class ContentTag:
    name: str
    is_selected: IntVar
