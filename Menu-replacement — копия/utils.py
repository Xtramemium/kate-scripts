import json


def read_json_file(file_path):
    """Читает JSON-файл."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def find_ids_by_name(data, target_names):
    """Ищет ID по имени."""
    return {entry["name"]: entry["id"] for entry in data if entry.get("name") in target_names}