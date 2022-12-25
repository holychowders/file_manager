import sqlite3
from sqlite3 import Cursor
from tkinter import Tk


def main() -> None:
    db_cursor = get_db_cursor()
    db_cursor.execute("")

    GUI().run()


def get_db_cursor() -> Cursor:
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()

    return cursor


class GUI:
    def __init__(self):
        gui = Tk()
        gui.title("File Manager")
        gui.iconbitmap("assets/main-icon-512px-colored.ico")
        gui.geometry("400x600")

        self.gui = gui

    def run(self) -> None:
        self.gui.mainloop()


if __name__ == "__main__":
    main()
