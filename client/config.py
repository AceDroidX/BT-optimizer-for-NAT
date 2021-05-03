import json
import os

path = 'config_client.json'


class ConfigManager():
    def __init__(self) -> None:
        if not os.path.exists(path):
            self.json = {}
            print("没有找到设置文件")
            return
        with open(path, 'r') as f:
            self.json = json.load(f)

    def read(self, key):
        if key in self.json:
            return self.json[key]
        else:
            print(f"设置文件中没有这个key:{key}")
            return None
