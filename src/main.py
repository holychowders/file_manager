import sqlite3
from dataclasses import dataclass
from sqlite3 import Cursor
from tkinter import Button, Checkbutton, IntVar, Label, Tk
from typing import List


def main() -> None:
    db_cursor = get_db_cursor()
    db_cursor.execute("")

    GUI(debug=False).run()


def get_db_cursor() -> Cursor:
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()

    return cursor


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

    def init_content_tags(self) -> None:
        self.tags: List[ContentTag] = []
        self.update_tags()
        self.add_tags_selection()

    def add_tags_selection(self):
        Label(self.gui, text="Tags").pack()

        for tag in self.tags:
            Checkbutton(self.gui, text=tag.name, variable=tag.is_selected).pack()

    def update_tags(self) -> None:
        # TODO: Get list of possible tags from database in order to create checkboxes for them.
        tags = ("Favorite", "Archive")

        for tag in tags:
            self.tags.append(ContentTag(tag, IntVar()))

    def debug(self) -> None:
        self.add_debug_button()

    def add_debug_button(self) -> None:
        Button(
            self.gui,
            text="Debug",
            command=lambda: print("\nDEBUG:") or [print(f"{tag.name} {tag.is_selected.get()}") for tag in self.tags],
        ).pack()


@dataclass
class ContentTag:
    name: str
    is_selected: IntVar


if __name__ == "__main__":
    main()
