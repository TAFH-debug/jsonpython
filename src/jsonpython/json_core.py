from json_objects import JsonParseError


def to_cls(cls: type, line: str | dict):
    new = cls.__new__(cls)
    if isinstance(line, dict):
        data = line
    else:
        data = parse(line)

    if '__annotations__' in vars(cls).keys():
        variables = vars(cls)['__annotations__']
        for i, j in data.items():
            if i in variables:
                if variables[i] in (str, int, bool, list, tuple, dict):
                    new.__setattr__(i, j)
                else:
                    new.__setattr__(i, to_cls(variables[i], j))
    else:
        for i, j in data.items():
            new.__setattr__(i, j)
    return new


def parse(line: str) -> dict:
    """
    Deserializing json.
    """

    last = ""
    data = {}
    counter = 0

    reading_name = False
    reading_value = False
    str_opened = False
    obj_brakets = 0
    value = ""
    name = ""

    for ch in line:
        input()
        if last == ":" and ch.isspace():
            continue
        if ch.isspace() and not reading_value:
            continue

        if last == "":
            if ch != "{":
                raise JsonParseError(f"Unexpected token at symbol {counter}, {ch}")
        else:
            if (last == "{" or last == "," or reading_name) and not reading_value:
                reading_name = True
                if ch == ":":
                    reading_value = True
                    reading_name = False
                else:
                    name += ch
            elif reading_value:
                if ch == "\"":
                    str_opened = not str_opened

                if ch == "{" and not str_opened:
                    print('a')
                    obj_brakets += 1
                elif ch == "}" and not str_opened:
                    print('b')
                    obj_brakets -= 1

                if (ch == "," or ch == "}") and not str_opened:
                    if obj_brakets != 0:
                        value += ch
                    else:
                        str_opened = False
                        reading_value = False
                        data[name[1:len(name) - 1]] = value.strip()
                        name = ""
                        value = ""
                else:
                    value += ch
            else:
                if ch != "," and ch != "}":
                    raise JsonParseError(f"Unexpected token at symbol {counter}, {ch}, {last}")
        last = ch
        counter += 1

    for i, j in data.items():
        if j.startswith('{'):
            a = parse(j)
            data[i] = a
        elif j.startswith("\"") and j.endswith("\""):
            data[i] = j[1:len(j) - 1]
        elif j.startswith("\'") and j.endswith("\'"):
            data[i] = j[1:len(j) - 1]
        elif j.startswith("[") and j.endswith("]"):
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
