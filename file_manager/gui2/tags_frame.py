from functools import partial
from tkinter import Checkbutton, Entry, Frame, LabelFrame, StringVar, Tk, Widget

import db
from gui2.files_frame import files_frame_interface


def add_tags_frame(gui: Tk) -> None:
    tags_frame = LabelFrame(gui, text="Search/Edit Tags", padx=2)
    query_results_frame: Frame = Frame(tags_frame)

    query = StringVar()
    query_box = Entry(tags_frame, textvariable=query)
    query_box.bind("<Return>", lambda _event: print("Pressed enter"))
    query_box.bind(
        "<KeyRelease>",
        lambda event: _handle_query_box_key_released(query, query_results_frame, event.keysym),
    )
    # Send initial empty query so that all available tags are displayed
    _handle_query_box_key_released(query, query_results_frame, "")

    tags_frame.grid(row=0, column=0, padx=2)
    query_box.grid()
    query_results_frame.grid(sticky="w")


def _handle_query_box_key_released(query: StringVar, query_results_frame: Widget, key_released: str) -> None:
    if key_released == "Tab":
        return

    _display_tag_query_results(query.get().strip(), query_results_frame)


def _display_tag_query_results(query: str, query_results_frame: Widget) -> None:
    tag_query_results = _get_tag_query_results(query)

    for old_tag_button in query_results_frame.winfo_children():
        old_tag_button.destroy()

    # FIXME: Cycling through elements via Tab in the Tags frame should start with the query box before buttons
    # FIXME: If buttons are focused, allow pressing Q to still quit app
    for tag in tag_query_results:
        Checkbutton(
            query_results_frame,
            text=tag.name,
            variable=tag.is_selected,
            command=partial(_handle_tag_selection, tag),
        ).grid(sticky="w")

    query_results_frame.update_idletasks()


def _get_tag_query_results(query: str) -> list[db.Tag]:
    # FIXME: Only fetch tags when the db has changed. For example, if we only allow modifying the db for certain
    # behaviors, we might check to see if those behaviors occurred and then cache a fresh fetch
    available_tags = db.fetch_unhidden_tags()
    results = []

    case_sensitive = _has_upper(query)
    for tag in available_tags:
        name_to_match = tag.name.casefold() if not case_sensitive else tag.name
        matches_query = set(query).issubset(set(name_to_match))

        if matches_query:
            results.append(tag)

    return results


def _handle_tag_selection(tag: db.Tag) -> None:
    db.toggle_tag_selection(tag)
    files_frame_interface.update()


def _has_upper(string: str) -> bool:
    return any(char.isupper() for char in string)
