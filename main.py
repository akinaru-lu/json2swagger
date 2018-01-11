import json
import re

from collections import OrderedDict


# Data types
# https://swagger.io/docs/specification/data-models/data-types/
String = "string"
Integer = "integer"
Number = "number"
Boolean = "boolean"
Object = "object"
Array = "array"


def read() -> str:
    data = []
    try:
        while True:
            data.append(input())
    except EOFError:
        return '\n'.join(data)


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


def to_swagger_format(data: OrderedDict) -> OrderedDict:
    new_data = OrderedDict()
    for k, v in data.items():
        t = type_of(v)
        if t == Object:
            new_data[k] = as_object(v)
        elif t == Array:
            new_data[k] = as_array(v)
        else:
            new_data[k] = as_default(v)
    return new_data


def to_swagger_format_str(data: OrderedDict, indent: int=2) -> str:
    swagger_json = to_swagger_format(data)
    return json.dumps(swagger_json, indent=indent)


def as_default(v) -> OrderedDict:
    return OrderedDict({
        "type": type_of(v),
        "example": v,
    })


def as_object(v: OrderedDict) -> OrderedDict:
    return OrderedDict({
        "type": type_of(v),
        "properties": to_swagger_format(v),
    })


def as_array(v: list) -> OrderedDict:
    try:
        item = v[0]
    except IndexError:
        item = None
    return OrderedDict({
        "type": type_of(v),
        "items": as_object(item),
    })


def output_as_yml(data: OrderedDict, prefix: str="", indent: str="  "):
    for k, v in data.items():
        print('{}{}:'.format(prefix, k))
        if type(v) == OrderedDict:
            output_as_yml(v, prefix=prefix + indent)
        elif type(v) == Array:
            pass
        else:
            print('{}{}'.format(prefix+indent, formatted(v)))


def str_is_num(s: str) -> bool:
    pattern = "^\d+(\.\d+)?$"
    return re.match(pattern, s) is not None


def formatted(v) -> str:
    """
    # format the value as the rule as following:
    - ""                     => ''
    - "This is a string\r\n" => This is a string\r\n
    - "123456"               => '123456'
    - 123456                 => 123456
    """
    t = type_of(v)
    if t == String:
        # if it can be casted to a number?
        if not v:  # if empty
            return "''"
        if str_is_num(v):  # if numeric
            return "'{}'".format(v)
    return repr(v).strip("'")


if __name__ == '__main__':
    src = read()
    data = json.loads(src, object_pairs_hook=OrderedDict)
    data = to_swagger_format(data)
    output_as_yml(data)
