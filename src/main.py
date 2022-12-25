import sqlite3


def main() -> None:
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()

    cursor.execute("")

    print(connection)


if __name__ == "__main__":
    main()
