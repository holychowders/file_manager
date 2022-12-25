import sqlite3
from tkinter import Tk


def main() -> None:
    gui = init_gui()

    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    cursor.execute("")
    print(connection)

    gui.mainloop()


def init_gui() -> Tk:
    root = Tk()
    root.title("File Manager")
    root.iconbitmap("assets/main-icon-512px-colored.ico")
    root.geometry("400x600")

    return root


if __name__ == "__main__":
    main()
