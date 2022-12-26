import os
from dataclasses import dataclass
from functools import partial
from tkinter import NW, TOP, Button, Checkbutton, Entry, IntVar, Label, N, Tk
from typing import List

from db import fetch_files_from_db, fetch_tags_from_db


class GUI:
    def __init__(self, debug=False):
        gui = Tk()
        gui.title("File Manager")
        gui.iconbitmap("assets/main-icon-512px-colored.ico")
        gui.geometry("600x600")

        self.gui = gui

        if debug:
            self.debug()

        self.add_search_bar()
        self.init_content_tags_section()
        self.init_file_results_section()

    def run(self) -> None:
        self.gui.mainloop()

    # Tags stuff

    def init_content_tags_section(self) -> None:
        self.tags: List[ContentTag] = []
        self.load_tags_from_db()
        self.add_tags_selection()

    def add_tags_selection(self):
        Label(self.gui, text="Tags").pack(anchor=NW)
        Entry(self.gui, width=20).pack(anchor=NW, ipadx=1, ipady=1)

        for tag in self.tags:
            Checkbutton(self.gui, text=tag.name, variable=tag.is_selected).pack(anchor=NW)

    def load_tags_from_db(self) -> None:
        tags = fetch_tags_from_db()

        for tag in tags:
            self.tags.append(ContentTag(tag, IntVar()))

    # Search bar

    def add_search_bar(self) -> None:
        Entry(self.gui, width=35).pack(side=TOP, anchor=N, ipadx=1, ipady=1)

    # File results stuff

    def init_file_results_section(self) -> None:
        self.file_results: List[FileResult] = []
        self.load_files_from_db()
        self.add_file_results()

    def load_files_from_db(self) -> None:
        files = fetch_files_from_db()

        for name, path in files:
            self.file_results.append(FileResult(name, path))

    def add_file_results(self) -> None:
        for file in self.file_results:
            Button(text=file.name, command=partial(os.startfile, file.path)).pack()

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


@dataclass
class FileResult:
    name: str
    path: str
