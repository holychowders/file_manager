import os
import subprocess
import sys
from functools import partial
from tkinter import Button, Entry, Frame, LabelFrame, StringVar, Tk, Widget

import db


# pylint: disable = R0903
class FilesFrameInterface:
    """Warning: The files frame must have been added prior in order for this interface to have been properly
    initialized. Use only after the files frame has been added.

    The purpose of this interface is to allow other frames to request an update when something relevant has changed.
    For example, if a tag has been selected, the files frame should be updated so that the query can be made with
    tag selections taken into account."""

    # TODO: These attributes should have a single underscore to indicate protected
    query: StringVar
    results_frame: Widget

    def update(self) -> None:
        _display_results(self.query, self.results_frame, "")


files_frame_interface = FilesFrameInterface()


def add_files_frame(gui: Tk) -> None:
    files_frame = LabelFrame(gui, text="Files", padx=2)

    query = StringVar()
    results_frame = Frame(files_frame)

    files_frame_interface.query = query
    files_frame_interface.results_frame = results_frame

    query_box = Entry(files_frame, textvariable=query)
    query_box.bind("<Return>", lambda _event: print("Pressed Enter"))
    query_box.bind("<KeyRelease>", lambda event: _display_results(query, results_frame, event.keysym))

    # Send empty query on init so all files are displayed at startup
    _display_results(query, results_frame, "")

    files_frame.grid(row=0, column=1, sticky="ns", padx=2)
    query_box.grid()
    results_frame.grid()


def _display_results(query: StringVar, results_frame: Widget, key_released: str) -> None:
    if key_released == "Tab":
        return

    file_query_results = _get_file_query_results(query.get().strip())

    for old_file_button in results_frame.winfo_children():
        old_file_button.destroy()

    max_file_name_length = 21

    # FIXME: Cycling through elements via Tab in the Files frame should start with the query box before buttons
    # FIXME: If buttons are focused, allow pressing Q to still quit app
    # TODO: Implement file searching
    for file in file_query_results:
        display_name = (
            file.name[: max_file_name_length - 3] + "..." if len(file.name) > max_file_name_length else file.name
        )
        # TODO: A button should not be created for files without a valid path. However, in case one is, the user should
        # be notified that the file they just tried to open couldn't be found, and a resolution must be offered.
        Button(results_frame, text=display_name, anchor="w", command=partial(open_file, file.path)).grid(sticky="ew")

    results_frame.update_idletasks()


def _get_file_query_results(_query: str) -> list[db.File]:
    results = []
    selected_tags = tuple(tag.name for tag in db.fetch_selected_tags())

    for file in db.fetch_files():
        # Partial matches
        has_selected_tags = set(selected_tags).issubset(file.tags)
        # Exact matches
        # has_selected_tags = set(file.tags).issubset(selected_tags)

        if has_selected_tags:
            results.append(file)

    return results


def open_file(filepath: str) -> None:
    if sys.platform == "win32":
        os.startfile(filepath)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filepath])
