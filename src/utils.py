from typing import List, Dict
import json


def load_txt(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return "".join([line.strip() for line in file if line.strip()])


def load_json(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return json.dumps(json.load(file))