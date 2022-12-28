import sys

import db
from gui import GUI


def main(debug: bool) -> None:
    db.init()
    GUI(debug).run()


if __name__ == "__main__":
    try:
        DEBUG = sys.argv[1] == "debug"
    except IndexError:
        DEBUG = False

    main(DEBUG)
