import os
from collections import namedtuple
from dataclasses import dataclass
from functools import partial
from tkinter import TOP, Button, Checkbutton, Entry, IntVar, LabelFrame, N, Tk
from typing import List

from db import fetch_files_from_db, fetch_tags_from_db

WidgetGridPosition = namedtuple("WidgetGridPosition", "row column")


class GUI:
    TAGS_FRAME_POS = WidgetGridPosition(0, 0)
    FILES_FRAME_POS = WidgetGridPosition(0, 1)

    def __init__(self, debug: bool = False) -> None:
        gui = Tk()
        gui.title("File Manager")
        gui.iconbitmap("assets/main-icon-512px-colored.ico")
        gui.geometry("600x600")

        self.gui = gui

        if debug:
            self.debug()

        self.init_tags_frame()
        self.init_files_frame()

    def run(self) -> None:
        self.gui.mainloop()

    # Tags stuff

    def init_tags_frame(self) -> None:
        self.tags: List[ContentTag] = []
        self.load_tags_from_db()
        self.add_tags_frame()

    def add_tags_frame(self) -> None:
        row, column = self.TAGS_FRAME_POS
        frame = LabelFrame(self.gui, text="Tags")
        frame.grid(row=row, column=column, padx=5, pady=5)

        self.add_tags_search_and_edit_subframe(frame)

        for tag in self.tags:
            Checkbutton(frame, text=tag.name, variable=tag.is_selected).grid()

    def add_tags_search_and_edit_subframe(self, tags_frame: LabelFrame) -> None:
        frame = LabelFrame(tags_frame, text="Search/Edit")
        frame.grid(padx=5, pady=5)

        Entry(frame, width=10).grid(row=0, column=0, padx=5, pady=10, ipadx=1, ipady=1)
        Button(frame, text="+/-").grid(row=0, column=1, padx=5, pady=5)

    def load_tags_from_db(self) -> None:
        tags = fetch_tags_from_db()

        for tag in tags:
            self.tags.append(ContentTag(tag, IntVar()))

    # File results stuff

    def init_files_frame(self) -> None:
        self.file_results: List[FileResult] = []
        self.load_files_from_db()
        self.add_files_frame()

    def load_files_from_db(self) -> None:
        files = fetch_files_from_db()

        for name, path in files:
            self.file_results.append(FileResult(name, path))

    def add_files_frame(self) -> None:
        row, column = self.FILES_FRAME_POS
        frame = LabelFrame(self.gui, text="Files")
        frame.grid(row=row, column=column, padx=5, pady=5)

        Entry(frame, width=35).pack(side=TOP, anchor=N, padx=5, pady=5, ipadx=1, ipady=1)

        for file in self.file_results:
            Button(frame, text=file.name, command=partial(os.startfile, file.path)).pack(padx=5, pady=5)

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
