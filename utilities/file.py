import json

def read_json(file_path):
    with open('path_to_file/person.json', 'r') as f:
        data = json.load(f)
    return data