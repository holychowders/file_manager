from tkinter import Tk

from gui2.tags_frame import add_tags_frame


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
