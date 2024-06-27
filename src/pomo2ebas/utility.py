
import json


def read_input_lines(io_wrapper):
    content = ""
    for line in io_wrapper:
        content += line

    if len(content.strip()) == 0:
        raise ValueError("Invalid input given.")
    return content


def is_json(input):
    try:
        json.loads(input)
        return True
    except ValueError as e:
        return False
    