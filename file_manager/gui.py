import os
from collections import namedtuple
from enum import Enum
from functools import partial
from logging import warning
from tkinter import TOP, Button, Checkbutton, Entry, LabelFrame, Menu, N, Tk

import db

WidgetGridPosition = namedtuple("WidgetGridPosition", "row column")

Colorscheme = Enum("Colorscheme", ["LIGHT", "DARK"])


# pylint: disable = R0903
class GUI:
    DEFAULT_COLORSCHEME = Colorscheme.LIGHT
    TAGS_FRAME_POS = WidgetGridPosition(0, 0)
    FILES_FRAME_POS = WidgetGridPosition(0, 1)

    def __init__(self, colorscheme: Colorscheme = DEFAULT_COLORSCHEME, debug: bool = False) -> None:
        self._init_colorscheme(colorscheme)
        self._init_root()
        self._add_menu_bar()
        self._handle_debug_init(debug)
        self._init_tags_frame()
        self._add_files_frame()

    def run(self) -> None:
        self.gui.mainloop()

    def _init_root(self) -> None:
        gui = Tk()
        gui.title("File Manager")
        gui.iconbitmap("assets/main-icon-512px-colored.ico")
        gui.geometry("600x600")
        gui.configure(bg=self.bg_color)

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

    def _init_tags_frame(self) -> None:
        row, column = self.TAGS_FRAME_POS

        frame = LabelFrame(self.gui, text="Tags", bg=self.bg_color, fg=self.fg_color)
        frame.grid(row=row, column=column, padx=5, pady=5)

        self._add_tags_search_and_edit_subframe(frame)
        self._add_tags_selection_clear_button(frame)
        self._populate_tags_in_tags_frame(frame)

    def _add_tags_search_and_edit_subframe(self, tags_frame: LabelFrame) -> None:
        frame = LabelFrame(tags_frame, text="Search/Edit", bg=self.bg_color, fg=self.fg_color)
        frame.grid(padx=5, pady=5)

        entry = Entry(frame, width=10, insertbackground=self.fg_color, bg=self.bg_color, fg=self.fg_color)
        entry.grid(row=0, column=0, padx=5, pady=10, ipadx=1, ipady=1)

        Button(
            frame,
            text="+/-",
            command=partial(self._toggle_tag_is_visible, tags_frame, entry),
            bg=self.bg_color,
            fg=self.fg_color,
            activebackground=self.bg_color,
            activeforeground=self.fg_color,
        ).grid(row=0, column=1, padx=5, pady=5)

    def _add_tags_selection_clear_button(self, tags_frame: LabelFrame) -> None:
        Button(
            tags_frame,
            text="Clear Selections",
            command=self._clear_tag_selections,
            bg=self.bg_color,
            fg=self.fg_color,
            activebackground=self.bg_color,
            activeforeground=self.fg_color,
        ).grid()

    def _toggle_tag_is_visible(self, tags_frame: LabelFrame, entry: Entry) -> None:
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

        self._update_tags_in_tags_frame(tags_frame)

    def _update_tags_in_tags_frame(self, frame: LabelFrame) -> None:
        self._clear_frame(frame)
        self._init_tags_frame()

    def _clear_frame(self, frame: LabelFrame) -> None:
        frame.destroy()
        if hasattr(frame, "pack_forget"):
            frame.pack_forget()

    def _populate_tags_in_tags_frame(self, tags_frame: LabelFrame) -> None:
        tags = db.fetch_tags()
        for tag in tags:
            if not tag.is_hidden:
                Checkbutton(
                    tags_frame,
                    text=tag.name,
                    variable=tag.is_selected,
                    command=partial(db.toggle_tag_selection, tag),
                    selectcolor=self.bg_color,
                    bg=self.bg_color,
                    fg=self.fg_color,
                    activebackground=self.bg_color,
                    activeforeground=self.fg_color,
                ).grid()

    def _clear_tag_selections(self) -> None:
        db.clear_all_tag_selections()
        # Should there be a self.clear_frame(tags_frame) here?
        self._init_tags_frame()

    # File results stuff

    def _add_files_frame(self) -> None:
        row, column = self.FILES_FRAME_POS
        frame = LabelFrame(self.gui, text="Files", bg=self.bg_color, fg=self.fg_color)
        frame.grid(row=row, column=column, padx=5, pady=5)

        Entry(frame, width=35, insertbackground=self.fg_color, bg=self.bg_color, fg=self.fg_color).pack(
            side=TOP, anchor=N, padx=5, pady=5, ipadx=1, ipady=1
        )

        files = db.fetch_files()
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
