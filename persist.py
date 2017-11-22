import json

settings = {}


def save(file_path):
    global settings
    with open(file_path, 'w') as outfile:
        json.dump(settings, outfile, indent=2, sort_keys=True)


def load(file_path):
    global settings
    try:
        with open(file_path) as data_file:
            settings = json.load(data_file)
    except Exception as e:
        pass
