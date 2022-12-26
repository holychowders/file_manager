from dataclasses import dataclass
from tkinter import Button, Checkbutton, IntVar, Label, Tk
from typing import List

from db import fetch_files_from_db, fetch_tags_from_db


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
