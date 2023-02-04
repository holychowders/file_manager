from tkinter import Checkbutton, Entry, Frame, LabelFrame, StringVar, Tk, Widget

from db import Tag, fetch_unhidden_tags


def run() -> None:
    gui = Tk()
    gui.title("File Manager")
    gui.iconbitmap("assets/main-icon-512px-colored.ico")
    gui.rowconfigure(0, weight=1)
    gui.columnconfigure(1, weight=1)

    gui.bind("<Escape>", lambda _event: handle_pressed_escape(gui))
    gui.bind("q", lambda _event: handle_pressed_q(gui))

    add_tags_frame(gui)

    gui.mainloop()


def handle_pressed_escape(gui: Tk) -> None:
    gui.focus_set()


def handle_pressed_q(gui: Tk) -> None:
    if gui.focus_get() == gui:
        gui.quit()


def add_tags_frame(gui: Tk) -> None:
    # TODO: Replace this and the query frame with a single "Search/Edit Tags" frame
    tags_frame = LabelFrame(gui, text="Tags")
    query_frame = LabelFrame(tags_frame, text="Search/Edit")
    query_results_frame = Frame(query_frame)

    query = StringVar()
    query_box = Entry(query_frame, textvariable=query)
    query_box.bind("<Return>", lambda _event: print("Pressed enter"))
    query_box.bind(
        "<KeyRelease>", lambda event: handle_query_box_key_released(query.get(), query_results_frame, event.keysym)
    )
    # Send initial empty query so that all available tags are displayed
    handle_query_box_key_released("", query_results_frame, "")

    tags_frame.grid()
    query_frame.grid()
    query_box.grid()
    query_results_frame.grid(sticky="w")


def handle_query_box_key_released(query: str, query_results_frame: Widget, key_released: str) -> None:
    if key_released == "Tab":
        return

    display_tag_query_results(query, query_results_frame)


def display_tag_query_results(query: str, query_results_frame: Widget) -> None:
    tag_query_results = get_tag_query_results(query)

    for old_tag_button in query_results_frame.winfo_children():
        old_tag_button.destroy()

    # FIXME: Cycling through elements via Tab in the Tags frame should start with the query box before buttons
    # FIXME: If buttons are focused, allow pressing Q to still quit app
    for tag in tag_query_results:
        Checkbutton(query_results_frame, text=tag.name).grid(sticky="w")

    query_results_frame.update_idletasks()


def get_tag_query_results(query: str) -> list[Tag]:
    # FIXME: Only fetch tags when the db has changed. For example, if we only allow modifying the db for certain
    # behaviors, we might check to see if those behaviors occurred and then cache a fresh fetch
    available_tags = fetch_unhidden_tags()
    results = []

    case_sensitive = has_upper(query)
    for tag in available_tags:
        name_to_match = tag.name.casefold() if not case_sensitive else tag.name
        matches_query = set(query).issubset(set(name_to_match))

        if matches_query:
            results.append(tag)
            print(tag.name)

    return results


def has_upper(string: str) -> bool:
    for char in string:
        if char.isupper():
            return True

    return False
