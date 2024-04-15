import json

def parse(filename):
    return {}

def parse_json(filename):
    with open(filename, 'r') as file:
        parsed_dict = json.load(file)
    return parsed_dict