from .parser import parse


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
