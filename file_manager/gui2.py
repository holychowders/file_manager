from tkinter import Entry, LabelFrame, StringVar, Tk


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
    tags_frame = LabelFrame(gui, text="Tags")
    tags_frame.grid()

    query_frame = LabelFrame(tags_frame, text="Search/Edit")
    query_frame.grid()

    query = StringVar()
    query_box = Entry(query_frame, textvariable=query)
    query_box.bind("<Return>", lambda _event: print("Pressed enter"))
    query_box.grid()
