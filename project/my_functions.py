from typing import Callable


Callback = Callable[[str], str]


def my_upper_callback(callback: Callback) -> str:
    return callback("This is a test").upper()


def my_upper_file(filename: str) -> str:
    with open(filename, "r") as file:
        content = file.read()
        return content.upper()


def my_upper_readlines(filename: str) -> str:
    with open(filename, "r") as file:
        content = file.readlines()
        return "\n".join([x.strip().upper() for x in content]) + "\n"


def my_writer(filename: str, content: str) -> None:
    with open(filename, "w") as file:
        file.write(content)
