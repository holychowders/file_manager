import sys

from src.main import main

if __name__ == "__main__":
    try:
        DEBUG = sys.argv[1] == "debug"
    except IndexError:
        DEBUG = False

    main(DEBUG)
