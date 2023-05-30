import json


def load_data(path: str):
    with open(path, 'r') as file_input:
        return json.loads(file_input.read())

def save_data(path: str, data):
    with open(path, 'w') as file_output:
        file_output.write(
            json.dumps(data, indent=2)
        )
