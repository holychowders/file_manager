import os
import tkinter
from collections import namedtuple
from enum import Enum
from functools import partial
from logging import warning
from tkinter import (
    TOP,
    Button,
    Checkbutton,
    E,
    Entry,
    Label,
    LabelFrame,
    Menu,
    N,
    S,
    StringVar,
    Tk,
    W,
)
from typing import List

import db

WidgetGridPosition = namedtuple("WidgetGridPosition", "row column")

Colorscheme = Enum("Colorscheme", ["LIGHT", "DARK"])


# pylint: disable = R0903
class GUI:
    DEFAULT_COLORSCHEME = Colorscheme.LIGHT
    TAGS_FRAME_POS = WidgetGridPosition(0, 0)
    FILES_FRAME_POS = WidgetGridPosition(0, 1)
    SELECTED_FILE_FRAME_POS = WidgetGridPosition(0, 2)

    def __init__(self, colorscheme: Colorscheme = DEFAULT_COLORSCHEME, debug: bool = False) -> None:
        self._init_colorscheme(colorscheme)
        self._init_root()
        self._add_menu_bar()
        self._handle_debug_init(debug)
        self._init_tags_frame()
        self._init_files_frame()
        self._init_selected_file_frame()

    def run(self) -> None:
        self.gui.mainloop()

    def _init_root(self) -> None:
        gui = Tk()
        gui.title("File Manager")
        gui.iconbitmap("assets/main-icon-512px-colored.ico")
        gui.configure(bg=self.bg_color)
        gui.rowconfigure(0, weight=1)
        gui.columnconfigure(1, weight=1)

        self.gui: Tk = gui

    def _init_colorscheme(self, colorscheme: Colorscheme) -> None:
        self.colorscheme = colorscheme

        match self.colorscheme:
            case Colorscheme.DARK:
                self.bg_color = "black"
                self.fg_color = "white"
            case Colorscheme.LIGHT:
                self.bg_color = "white"
                self.fg_color = "black"
            case other:
                warning(f"Colorscheme '{other}' not valid. Using default '{self.DEFAULT_COLORSCHEME}'.")
                self._init_colorscheme(self.DEFAULT_COLORSCHEME)

    def _add_menu_bar(self) -> None:
        menu_bar = Menu(self.gui, tearoff=0, bg=self.bg_color, fg=self.fg_color)

        # "View" -> "Colorscheme" -> colorschemes
        view = Menu(menu_bar, tearoff=0, bg=self.bg_color, fg=self.fg_color)
        colorscheme = Menu(view, tearoff=0, bg=self.bg_color, fg=self.fg_color)
        colorscheme.add_command(label="Light", command=partial(self._switch_colorscheme, Colorscheme.LIGHT))
        colorscheme.add_command(label="Dark", command=partial(self._switch_colorscheme, Colorscheme.DARK))

        view.add_cascade(label="Colorscheme", menu=colorscheme, background=self.bg_color, foreground=self.fg_color)
        menu_bar.add_cascade(label="View", menu=view, background=self.bg_color, foreground=self.fg_color)

        self.gui.configure(menu=menu_bar)

    def _switch_colorscheme(self, colorscheme: Colorscheme) -> None:
        self._reinit(colorscheme=colorscheme, debug=self.debug)

    def _reinit(self, colorscheme: Colorscheme, debug: bool) -> None:
        self.gui.destroy()
        # pylint: disable = C2801
        self.__init__(colorscheme=colorscheme, debug=debug)  # type: ignore[misc]

    def _handle_debug_init(self, debug: bool) -> None:
        self.debug = debug

        if self.debug:
            self._add_debug_button()

    # Tags stuff

    def _init_tags_frame(self, current_tags_search: str = "", was_focused_last: bool = False) -> None:
        row, column = self.TAGS_FRAME_POS

        frame = LabelFrame(self.gui, text="Tags", bg=self.bg_color, fg=self.fg_color)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky=E + W + N + S)

        self.tags_frame = frame

        self.tags_search = StringVar()
        self._add_tags_search_and_edit_subframe(
            current_tags_search=current_tags_search, was_focused_last=was_focused_last
        )
        self._add_tags_selection_clear_button()
        self._populate_tags_in_tags_frame()

    def _add_tags_search_and_edit_subframe(self, current_tags_search: str, was_focused_last: bool) -> None:
        frame = LabelFrame(self.tags_frame, text="Search/Edit", bg=self.bg_color, fg=self.fg_color)
        frame.grid(padx=5, pady=5)

        entry = Entry(
            frame,
            textvariable=self.tags_search,
            width=10,
            insertbackground=self.fg_color,
            bg=self.bg_color,
            fg=self.fg_color,
        )
        entry.bind("<Return>", lambda _event: self._toggle_tag_visibility(entry))
        entry.grid(row=0, column=0, padx=5, pady=10, ipadx=1, ipady=1)

        entry.insert(0, current_tags_search)
        if was_focused_last:
            entry.focus()

        self.tags_search.trace_add("write", lambda *_args: self._handle_tag_search())

        Button(
            frame,
            text="+/-",
            command=partial(self._toggle_tag_visibility, entry),
            bg=self.bg_color,
            fg=self.fg_color,
            activebackground=self.bg_color,
            activeforeground=self.fg_color,
        ).grid(row=0, column=1, padx=5, pady=5)

    def _handle_tag_search(self) -> None:
        self._clear_frame(self.tags_frame)
        self._init_tags_frame(current_tags_search=self.tags_search.get(), was_focused_last=True)

    def _add_tags_selection_clear_button(self) -> None:
        Button(
            self.tags_frame,
            text="Clear Selections",
            command=self._clear_tag_selections,
            bg=self.bg_color,
            fg=self.fg_color,
            activebackground=self.bg_color,
            activeforeground=self.fg_color,
        ).grid(padx=3, pady=(0, 3), sticky=E + W)

    def _toggle_tag_visibility(self, entry: Entry) -> None:
        """Toggle the visibility of the tag itself on the UI."""
        target = entry.get()

        if not target:
            return

        tags = db.fetch_tags()
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

        self._update_tags_in_tags_frame()

    def _update_tags_in_tags_frame(self) -> None:
        self._clear_frame(self.tags_frame)
        self._init_tags_frame()

    def _clear_frame(self, frame: LabelFrame) -> None:
        frame.destroy()
        if hasattr(frame, "pack_forget"):
            frame.pack_forget()

    def _populate_tags_in_tags_frame(self) -> None:
        for tag in self._get_visible_and_matching_tags():
            Checkbutton(
                self.tags_frame,
                text=tag.name,
                variable=tag.is_selected,
                command=partial(self._handle_tag_selection, tag),
                anchor=W,
                selectcolor=self.bg_color,
                bg=self.bg_color,
                fg=self.fg_color,
                activebackground=self.bg_color,
                activeforeground=self.fg_color,
            ).grid(padx=5, sticky=E + W)

    def _handle_tag_selection(self, tag: db.Tag) -> None:
        db.toggle_tag_selection(tag)
        self._clear_frame(self.files_frame)
        self._init_files_frame()

    def _clear_tag_selections(self) -> None:
        db.clear_all_tag_selections()

        self._clear_frame(self.tags_frame)
        self._init_tags_frame()

        self._clear_frame(self.files_frame)
        self._init_files_frame()

    def _get_visible_tags(self) -> List[db.Tag]:
        visible_tags = []

        for tag in db.fetch_tags():
            if not tag.is_hidden:
                visible_tags.append(tag)

        return visible_tags

    def _get_visible_and_matching_tags(self) -> List[db.Tag]:
        tags = []
        search = set(self.tags_search.get())

        # Become case-sensitive if at least one character in the search is uppercase.
        case_sensitive = False
        for char in search:
            if char.isupper():
                case_sensitive = True
                break

        for tag in db.fetch_tags():
            name = set(tag.name if case_sensitive else tag.name.lower())

            if not tag.is_hidden and search.issubset(name):
                tags.append(tag)

        return tags

    def _get_selected_tag_names(self) -> List[str]:
        selected_tags = []

        for tag in db.fetch_tags():
            if tag.is_selected.get():
                selected_tags.append(tag.name)

        return selected_tags

    # File results stuff

    def _init_files_frame(self) -> None:
        self.selected_file = None

        row, column = self.FILES_FRAME_POS

        frame = LabelFrame(self.gui, text="Files", bg=self.bg_color, fg=self.fg_color)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky=E + W + N + S)

        Entry(frame, width=35, insertbackground=self.fg_color, bg=self.bg_color, fg=self.fg_color).pack(
            side=TOP, anchor=N, fill="x", padx=5, pady=5, ipadx=1, ipady=1
        )

        selected_tags = set(self._get_selected_tag_names())

        for file in db.fetch_files():
            if selected_tags.issubset(file.tags):
                button = Button(
                    frame,
                    text=file.name,
                    command=partial(os.startfile, file.path),
                    bg=self.bg_color,
                    fg=self.fg_color,
                    activebackground=self.bg_color,
                    activeforeground=self.fg_color,
                )
                button.pack(fill="x", padx=3, pady=3)
                button.bind("<Button-3>", partial(self._update_selected_file_frame, file))

        self.files_frame = frame

    def _update_selected_file_frame(self, file: db.File, _args: tkinter.Event) -> None:
        # pylint: disable = W0201
        self.selected_file = file
        self._clear_frame(self.selected_file_frame)
        self._init_selected_file_frame()

    def _init_selected_file_frame(self) -> None:
        row, column = self.SELECTED_FILE_FRAME_POS

        frame = LabelFrame(self.gui, text="Selected File", bg=self.bg_color, fg=self.fg_color)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky=E + W + N + S)

        file = self.selected_file

        if not file:
            Label(frame, text="No file selected", padx=5, pady=5, bg=self.bg_color, fg=self.fg_color).pack(
                fill="x", padx=5, pady=5
            )
        else:
            for info in file.get_display_info():
                info_frame = LabelFrame(frame, text=info.title, padx=5, bg=self.bg_color, fg=self.fg_color)
                info_frame.pack(fill="x", padx=5, pady=5)
                Label(info_frame, text=info.info, padx=5, bg=self.bg_color, fg=self.fg_color).pack(padx=5, pady=5)

        self.selected_file_frame = frame

    # Debugging stuff

    def _add_debug_button(self) -> None:
        Button(
            self.gui,
            text="Debug",
            command=db.debug,
            bg=self.bg_color,
            fg=self.fg_color,
            activebackground=self.bg_color,
            activeforeground=self.fg_color,
        ).pack()
