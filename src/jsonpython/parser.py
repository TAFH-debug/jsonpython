CLOSING_TOKENS = [",", "}", "]"]

class JsonParseError(Exception):
    pass


class Tokenizer:

    def __init__(self, line: str):
        self._counter = 0
        self.line = line

    def next(self) -> str:
        try:
            temp = self.line[self._counter]
        except IndexError:
            raise JsonParseError("unexpected EOF")
        self._counter += 1
        return temp

    def cancel_last(self):
        self._counter -= 1

    def get_counter(self) -> int:
        return self._counter


def remove_spaces(line: str) -> str:
    result = ""
    is_str = False

    for i in line:
        if i == "\"":
            is_str = not is_str
        if i.isspace() and not is_str:
            continue
        result += i
    return result


def read_array(tokens) -> (list, Tokenizer):
    result = []

    token = tokens.next()

    if token != "[":
        raise JsonParseError(f"Unexpected token at {tokens.get_counter()}")

    while True:
        (value, tokens) = read_value(tokens)
        result.append(value)

        if tokens.next() == "]":
            break
    return result, tokens


def read_number(tokens) -> (float, Tokenizer):
    result = ""

    while True:
        token = tokens.next()

        if token in CLOSING_TOKENS:
            tokens.cancel_last()
            break
        result += token
    return float(result), tokens


def read_value(tokens: Tokenizer) -> (object, Tokenizer):
    token = tokens.next()
    tokens.cancel_last()

    if token == "\"":
        return read_string(tokens)
    elif token.isdigit():
        return read_number(tokens)
    elif token == "{":
        return read_object(tokens)
    elif token == "[":
        return read_array(tokens)
    else:
        raise JsonParseError(f"Unexpected token at {tokens.get_counter()}")


def read_string(tokens: Tokenizer) -> (str, Tokenizer):
    token = tokens.next()
    if token != "\"":
        raise JsonParseError(f"Unexpected token at {tokens.get_counter()}")

    result = ""
    while True:
        token = tokens.next()
        if token == "\"":
            break
        result += token

    return result, tokens


def read_object(tokens: Tokenizer) -> (dict, Tokenizer):
    result = {}

    token = tokens.next()

    if token != "{":
        raise JsonParseError(f"Unexpected token at {tokens.get_counter()}")

    while True:
        (key, tokens) = read_string(tokens)

        if tokens.next() != ":":
            raise JsonParseError(f"Unexpected token at {tokens.get_counter()}")

        (value, tokens) = read_value(tokens)

        result[key] = value

        if tokens.next() == "}":
            break

    return result, tokens


def parse(line: str) -> dict:
    """

    Parameters
    ----------
    line - :class 'str':
    Line to parse.

    Returns
    -------
    :class 'dict':
    Parsed json object.
    """
    tokenizer = Tokenizer(remove_spaces(line))
    return read_object(tokenizer)[0]


if __name__ == "__main__":
    print(parse(open("../../data.json").read()))
