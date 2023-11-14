import json


def save_to_file(object_to_save, filename):
    data = json.dumps(object_to_save, indent=4)
    with open(filename, 'w') as file:
        file.write(data)


def load_from_file(file, object_hook):
    with open(file, 'r') as file:
        return json.load(file, object_hook=object_hook)
