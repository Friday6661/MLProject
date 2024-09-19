import json

class JsonHelper():

    def load_config(self, config_name: str, action: str = "r") -> dict:
        with open(config_name, action) as file:
            return json.load(file)
