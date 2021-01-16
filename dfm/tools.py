import os


def here(path: str) -> str:
    return os.path.dirname(__file__) + "/" + path
