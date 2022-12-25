import sqlite3
from sqlite3 import Cursor
from tkinter import Tk


def main() -> None:
    db_cursor = get_db_cursor()
    db_cursor.execute("")

    build_gui().mainloop()


def get_db_cursor() -> Cursor:
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()

    return cursor


def build_gui() -> Tk:
    gui = Tk()
    gui.title("File Manager")
    gui.iconbitmap("assets/main-icon-512px-colored.ico")
    gui.geometry("400x600")

    return gui


if __name__ == "__main__":
    main()
