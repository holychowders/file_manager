from tkinter import Tk


def run() -> None:
    gui = Tk()
    gui.title("File Manager")
    gui.iconbitmap("assets/main-icon-512px-colored.ico")
    gui.rowconfigure(0, weight=1)
    gui.columnconfigure(1, weight=1)

    gui.mainloop()
