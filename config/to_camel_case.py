import re


def to_camel_case(snake_str):
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), snake_str)
