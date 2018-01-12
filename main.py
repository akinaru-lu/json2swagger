import argparse
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


def as_swagger_json(data) -> OrderedDict:
    t = type_of(data)
    if t == Object:
        return as_object(data)
    elif t == Array:
        return as_array(data)
    raise ValueError('invalid json data')


def _to_swagger_format(data) -> OrderedDict:
    if type_of(data) == Array:
        return as_array(data)
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
    swagger_json = as_swagger_json(data)
    return json.dumps(swagger_json, indent=indent)


def as_default(v) -> OrderedDict:
    if v is None:
        return as_object(OrderedDict())
    return OrderedDict({
        "type": type_of(v),
        "example": v,
    })


def as_object(v) -> OrderedDict:
    if type_of(v) == Array:
        return as_array(v)
    od = OrderedDict()
    od["type"] = type_of(v)
    child = _to_swagger_format(v)
    if child:
        od["properties"] = child
    return od


def as_array(v: list) -> OrderedDict:
    if type_of(v) == Object:
        return as_object(v)
    od = OrderedDict()
    od["type"] = type_of(v)
    try:
        od["items"] = as_object(v[0])
    except IndexError:
        return od
    return od


def output_as_yml(data: OrderedDict, prefix: str='', indent: str='  '):
    if not data:
        return
    for k, v in data.items():
        print('{}{}:'.format(prefix, k))
        if type(v) == OrderedDict:
            output_as_yml(v, prefix=prefix+indent, indent=indent)
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
    elif t == Boolean:
        if v:
            return 'true'
        return 'false'
    return repr(v).strip("'")


def run(prefix: str='', indent: str='  '):
    src = read()
    if not src:
        raise ValueError("empty input")

    data = json.loads(src, object_pairs_hook=OrderedDict)
    data = as_swagger_json(data)
    output_as_yml(data, prefix=prefix, indent=indent)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prefix', '-p', type=str, default='')
    parser.add_argument('--indent', '-i', type=str, default='  ')

    args = parser.parse_args()
    run(prefix=args.prefix, indent=args.indent)
