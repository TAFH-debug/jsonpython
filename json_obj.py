from typing import Final

JSON_EXTENTION: Final = "json"


def get_json_object(path: str):
    """
    Deserializes json from file and returns a json object.
    """

    with open(path, "r") as file:
        src = file.read()
