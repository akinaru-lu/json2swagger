import json
from collections import OrderedDict


def read() -> str:
    data = []
    try:
        while True:
            data.append(input())
    except EOFError:
        return '\n'.join(data)


String = "string"
Integer = "integer"
Number = "number"
Boolean = "boolean"
Object = "object"
Array = "array"


def type_of(o: object) -> str:
    name = type(o).__name__
    if name == 'str':
        return String
    elif name == 'int':
        return Integer
    elif name == 'float':
        return Number
    elif name == 'bool':
        return Boolean
    elif name == 'OrderedDict':
        return Object
    elif name == 'list':
        return Array
    return 'unknown type: ' + name


if __name__ == '__main__':
    src = read()
    data = json.loads(src, object_pairs_hook=OrderedDict)
    t = type(data)

    for k, v in data.items():
        print(k, v, type_of(v))
