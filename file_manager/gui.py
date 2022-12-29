import os
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from functools import partial
from logging import warning
from tkinter import TOP, Button, Checkbutton, Entry, IntVar, LabelFrame, N, Tk
from typing import List

import db


@dataclass
class ContentTag:
    name: str
    is_hidden: bool
    is_selected: IntVar


@dataclass
class FileResult:
    name: str
    path: str


WidgetGridPosition = namedtuple("WidgetGridPosition", "row column")

Colorscheme = Enum("Colorscheme", ["LIGHT", "DARK"])


class GUI:
    TAGS_FRAME_POS = WidgetGridPosition(0, 0)
    FILES_FRAME_POS = WidgetGridPosition(0, 1)

    def __init__(self, colorscheme: Colorscheme = Colorscheme.LIGHT, debug: bool = False) -> None:
        self.init_colorscheme(colorscheme)

        self.init_root()

        if debug:
            self.debug()

        self.init_tags_frame()
        self.add_files_frame()

    def run(self) -> None:
        self.gui.mainloop()

    def init_root(self) -> None:
        gui = Tk()
        gui.title("File Manager")
        gui.iconbitmap("assets/main-icon-512px-colored.ico")
        gui.geometry("600x600")
        gui.configure(bg=self.bg_color)

        self.gui: Tk = gui

    def init_colorscheme(self, colorscheme: Colorscheme) -> None:
        match colorscheme:
            case Colorscheme.DARK:
                self.bg_color = "black"
                self.fg_color = "white"
            case Colorscheme.LIGHT:
                self.bg_color = "white"
                self.fg_color = "black"
            case other:
                warning(f"Colorscheme '{other}' not valid. Using default.")
                self.bg_color = "white"
                self.fg_color = "black"

    # Tags stuff

    def init_tags_frame(self) -> None:
        row, column = self.TAGS_FRAME_POS

        frame = LabelFrame(self.gui, text="Tags", bg=self.bg_color, fg=self.fg_color)
        frame.grid(row=row, column=column, padx=5, pady=5)

        self.add_tags_search_and_edit_subframe(frame)
        self.add_tags_selection_clear_button(frame)
        self.populate_tags_in_tags_frame(frame)

    def add_tags_search_and_edit_subframe(self, tags_frame: LabelFrame) -> None:
        frame = LabelFrame(tags_frame, text="Search/Edit", bg=self.bg_color, fg=self.fg_color)
        frame.grid(padx=5, pady=5)

        entry = Entry(frame, width=10, bg=self.bg_color, fg=self.fg_color)
        entry.grid(row=0, column=0, padx=5, pady=10, ipadx=1, ipady=1)

        Button(
            frame,
            text="+/-",
            command=partial(self.toggle_tag_visibility_in_db, tags_frame, entry),
            bg=self.bg_color,
            fg=self.fg_color,
            activebackground=self.bg_color,
            activeforeground=self.fg_color,
        ).grid(row=0, column=1, padx=5, pady=5)

    def add_tags_selection_clear_button(self, tags_frame: LabelFrame) -> None:
        Button(
            tags_frame,
            text="Clear Selections",
            command=self.clear_tag_selections,
            bg=self.bg_color,
            fg=self.fg_color,
            activebackground=self.bg_color,
            activeforeground=self.fg_color,
        ).grid()

    def toggle_tag_visibility_in_db(self, tags_frame: LabelFrame, entry: Entry) -> None:
        """Toggle the visibility of the tag itself on the UI."""
        target = entry.get()

        if not target:
            return

        tags = self.fetch_tags_from_db()
        is_target_in_tags = False
        for tag in tags:
            if tag.name == target:
                is_target_in_tags = True

                if tag.is_hidden:
                    db.enable_tag_visibility(target)
                else:
                    db.disable_tag_selection(target)
                    db.disable_tag_visibility(target)
        if not is_target_in_tags:
            db.create_tag(target)

        self.update_tags_in_tags_frame(tags_frame)

    def update_tags_in_tags_frame(self, frame: LabelFrame) -> None:
        self.clear_frame(frame)
        self.init_tags_frame()

    def clear_frame(self, frame: LabelFrame) -> None:
        frame.destroy()
        frame.pack_forget()

    def populate_tags_in_tags_frame(self, tags_frame: LabelFrame) -> None:
        tags = self.fetch_tags_from_db()
        for tag in tags:
            if not tag.is_hidden:
                Checkbutton(
                    tags_frame,
                    text=tag.name,
                    variable=tag.is_selected,
                    command=partial(self.toggle_tag_selection_in_db, tag),
                    selectcolor=self.bg_color,
                    bg=self.bg_color,
                    fg=self.fg_color,
                    activebackground=self.bg_color,
                    activeforeground=self.fg_color,
                ).grid()

    def toggle_tag_selection_in_db(self, tag: ContentTag) -> None:
        db.get_cursor().execute(
            f"UPDATE tags SET is_selected={tag.is_selected.get()} WHERE name='{tag.name}'"
        ).connection.commit()

    def clear_tag_selections(self) -> None:
        self.clear_tag_selections_in_db()
        # Should there be a self.clear_frame(tags_frame) here?
        self.init_tags_frame()

    def clear_tag_selections_in_db(self) -> None:
        db.get_cursor().execute("UPDATE tags SET is_selected=0 ").connection.commit()

    @staticmethod
    def fetch_tags_from_db() -> List[ContentTag]:
        tags = db.fetch_tags()
        content_tags = []

        for tag, is_hidden, is_selected_in_db in tags:
            is_selected = IntVar()
            is_selected.set(is_selected_in_db)

            content_tags.append(ContentTag(name=tag, is_hidden=is_hidden, is_selected=is_selected))

        return content_tags

    # File results stuff

    def add_files_frame(self) -> None:
        row, column = self.FILES_FRAME_POS
        frame = LabelFrame(self.gui, text="Files", bg=self.bg_color, fg=self.fg_color)
        frame.grid(row=row, column=column, padx=5, pady=5)

        Entry(frame, width=35, bg=self.bg_color, fg=self.fg_color).pack(
            side=TOP, anchor=N, padx=5, pady=5, ipadx=1, ipady=1
        )

        files = self.fetch_files_from_db()
        for file in files:
            Button(
                frame,
                text=file.name,
                command=partial(os.startfile, file.path),
                bg=self.bg_color,
                fg=self.fg_color,
                activebackground=self.bg_color,
                activeforeground=self.fg_color,
            ).pack()

    @staticmethod
    def fetch_files_from_db() -> List[FileResult]:
        files = db.fetch_files()
        file_results = []

        for name, path in files:
            file_results.append(FileResult(name, path))

        return file_results

    # Debugging stuff

    def debug(self) -> None:
        self.add_debug_button()

    def add_debug_button(self) -> None:
        Button(
            self.gui,
            text="Debug",
            command=debug_db,
            bg=self.bg_color,
            fg=self.fg_color,
            activebackground=self.bg_color,
            activeforeground=self.fg_color,
        ).pack()


def debug_db() -> None:
    print("\nDB DEBUG:")
    print("files:\n", db.fetch_files())
    print("\ntags:\n", db.fetch_tags())
