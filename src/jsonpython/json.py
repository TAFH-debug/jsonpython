from .json_core import *


def from_file(cls: type, path: str):
    """
    Parameters
    -------------
    cls: :class 'type':
        Class of object.
    path: :class 'str':
        Path to file.

    Returns
    -------------
    :class cls:
        Object that type is :param cls:.
    """

    with open(path, "r") as f:
        return to_cls(cls, f.read())


def write_object(ob: object, path: str):
    """
    Parameters
    --------------
    ob: :class 'object':
        Object to serialize and write.
    path: :class 'str':
        Path to file.
    """

    with open(path, "w") as f:
        f.write(to_json(ob))
