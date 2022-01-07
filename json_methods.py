from typing import Final
from json_objects import *
from json_core import *

JSON_EXTENTION: Final = "json"

def get_class(cls: type, path: str):
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

def write_object(ob: object, path: str, indent = 1, in_one_line = True):
    """
    Parameters
    --------------
    ob: :class 'object':
        Object to serialize and write.
    path: :class 'str':
        Path to file.
    indent: :class 'int':
        Indent.
    in_one_line: :class 'bool':
        Is write in one line.
    """

    with open(path, "w") as f:
        f.write(to_json(ob, indent = indent, in_one_line = in_one_line))

def get_json_object(path: str) -> JsonObject:
    """
    Deserializes json from file and returns a json object.

    Parameters
    --------------
    path: :class 'str':
        File location.

    Returns
    --------------
    :class 'JsonObject':
        Deserialized json object.
    """

    if path[-4:len(path)] != JSON_EXTENTION:
        raise NotAJsonFileError

    with open(path, "r") as file:
        return JsonObject(parse(file.read()))

class Company:
    age: int
    name: str
    count: int

class Car:
    model: str
    age: int
    company: Company

class Person:
    name: str
    age: int
    car: Car
    company: Company

if __name__ == "__main__":
    with open("data.json") as file:
        print(parse(file.read()))