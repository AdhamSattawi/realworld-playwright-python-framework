import json

def load_user_data(file_path: str):
    with open(file_path) as file:
        return json.load(file)