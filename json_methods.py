from typing import Final
from json_objects import JsonParseError

JSON_EXTENTION: Final = "json"


def get_json_object(path: str):
    """
    Deserializes json from file and returns a json object.
    """

    with open(path, "r") as file:
        return __parse(file.read())


# I don't know how it work. But it is work!
def __parse(line: str) -> dict:
    """
    First level parsing.
    """

    last = ""
    data = {}
    counter = 0
    readingName = False
    readingValue = False
    isObject = False
    value = ""
    name = ""
    for ch in line:
        if ch.isspace(): continue

        if last == "":
            if ch != "{":
                raise JsonParseError(f"Unexpected token at symbol {counter}, {ch}")
        else:
            if (last == "{" or last == "," or readingName) and not readingValue:
                readingName = True
                if ch == ":":
                    readingValue = True
                    readingName = False
                else:
                    name += ch
            elif readingValue:
                if ch == "{" and last == ":":
                    isObject = True
                if ch == "," or ch == "}":
                    if ch == "," and isObject:
                        value += ch
                    elif isObject:
                        readingValue = False
                        value += ch
                        data[name[1:len(name) - 1]] = value
                        isObject = False
                        name = ""
                        value = ""
                    else:
                        readingValue = False
                        data[name[1:len(name) - 1]] = value
                        isObject = False
                        name = ""
                        value = ""
                else:
                    value += ch
            else:
                if ch != "," and ch != "}":
                    raise JsonParseError(f"Unexpected token at symbol {counter}, {ch}, {last}")
        last = ch
        print(last)
        counter += 1

    for i, j in data.items():
        if j.startswith('{'):
            data[i] = __parse(j)
        elif j.startswith("\""):
            data[i] = j[1:len(j) - 1]

        else:
            try:
                data[i] = int(j)
            except ValueError:
                if j == "false":
                    data[i] = False
                elif j == "true":
                    data[i] = True
                else:
                    raise JsonParseError("Something went wrong.")
    return data
