import json
import os

path = 'config_client.json'


class ConfigManager():
    def __init__(self) -> None:
        if not os.path.exists(path):
            print("没有找到设置文件，将采用环境变量获取设置")
            self.json = os.environ
            return
        with open(path, 'r') as f:
            self.json = json.load(f)

    def read(self, key):
        if key in self.json:
            return self.json[key]
        else:
            print(f"设置中没有这个key:{key}")
            return None
