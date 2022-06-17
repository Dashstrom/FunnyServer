"""File call when module is called as script."""
from server import FileServer


def main() -> None:
    FileServer()


if __name__ == "__main__":
    main()
