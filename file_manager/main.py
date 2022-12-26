import sys

from db import init_db
from gui import GUI


def main(debug: bool) -> None:
    init_db()
    GUI(debug).run()


if __name__ == "__main__":
    try:
        DEBUG = sys.argv[1] == "debug"
    except IndexError:
        DEBUG = False

    main(DEBUG)
