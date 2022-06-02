def to_json(ob: object, indent=1, in_one_line=True, **kwargs) -> str:
    """
    Parameters
    ---------------
    indent: :class 'int':
        Indent in json string.
    in_one_line: :class 'bool':
        If true json string be wrote in one line.
    ob: :class 'object':
        Object that you want to serialize.

    Returns
    ---------------
    :class 'str':
        Serialized json string.
    """

    result = ""
    if isinstance(ob, str):
        return f"\"{ob}\""
    elif isinstance(ob, int):
        return str(ob)
    elif isinstance(ob, bool):
        if ob:
            return "true"
        else:
            return "false"
    elif isinstance(ob, (list, tuple, set)):
        result += "["
        for i in ob:
            if in_one_line:
                result += " " * indent + to_json(i) + ","
            else:
                pass

        result = result[0:len(result) - 1]
        result += "]"
    else:
        a = None
        if isinstance(ob, dict):
            a = ob
        else:
            a = vars(ob)
        result = JsonObject(a).serialize(indent, in_one_line, **kwargs)

    return result


class JsonObject:
    keys: tuple
    objects: tuple

    def serialize(self, indent=1, in_one_line=True, **kwargs):
        """
        Parameters
        ---------------------
        indent: :class 'int':
            Count of spaces in tab.
        in_one_line: :class 'bool':
            Is serialize to one line.

        Returns
        ---------------------
        :class 'str':
            Serialized json string.
        """

        result = "{"
        issub = "sub" in kwargs.keys()
        for i, j in zip(self.keys, self.objects):
            if in_one_line:
                result += " " * indent + f"\"{i}\": {to_json(j, indent, in_one_line)},"
            elif issub:
                result += "\n" + " " * (indent * kwargs[
                    'sub'] + indent) + f"\"{i}\": {to_json(j, indent, in_one_line, sub=kwargs['sub'] + 1)},"
            else:
                result += "\n" + " " * indent + f"\"{i}\": {to_json(j, indent, in_one_line, sub=2)},"

        result = result[0:len(result) - 1]

        if issub:
            result += "\n" + indent * kwargs['sub'] * " " + "}"
        elif not in_one_line:
            result += "\n" + "}"
        else:
            result += "}"

        return result

    def __init__(self, d: dict):
        """
        Parameters
        -----------------
        d: :class 'dict':
            Deserialized json dictionary.
        """

        self.keys = tuple(d.keys())
        self.objects = tuple(d.values())

    def __getitem__(self, item):
        """ x[key] <===> x.__getitem__(key) """

        return self.objects[self.keys.index(item)]

    def __setitem__(self, key, value):
        """
        x[key] = value
        x.__setitem__(key, value)
        """

        a = list(self.keys)
        b = list(self.objects)

        if key in a:
            idx = a.index(key)
            b[idx] = value
        else:
            a.append(key)
            b.append(value)

        self.keys = tuple(a)
        self.objects = tuple(b)
        del a
        del b

    def __str__(self):
        """
        Returns
        --------------
        :class 'str':
            Deserialized json string.
        """

        return self.serialize()
