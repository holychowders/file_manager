import sys

import db
from gui import GUI
from gui2 import run as gui2_run


def main(use_gui2: bool) -> None:  # noqa: FBT001
    db.init()

    if use_gui2:
        gui2_run()
    else:
        GUI().run()


if __name__ == "__main__":
    try:
        USE_GUI2 = sys.argv[1] == "gui2"
    except IndexError:
        USE_GUI2 = False

    main(use_gui2=USE_GUI2)
