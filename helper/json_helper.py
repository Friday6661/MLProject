import json

class JsonHelper():

    def load_config(self, config_name: str, action: str = "r") -> dict:
        with open(config_name, action) as file:
            return json.load(file)
        
    def load_view_queries_from_json(self, file_path: str) -> dict:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return {view_name: view_info["query"] for view_name, view_info in data["views"].items()}
