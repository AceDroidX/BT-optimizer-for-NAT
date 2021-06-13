import json
import os
import logging

path = 'config_server.json'


class ConfigManager():
    def __init__(self) -> None:
        if not os.path.exists(path):
            logging.info("没有找到设置文件，将采用环境变量获取设置")
            self.json = os.environ
            return
        with open(path, 'r') as f:
            self.json = json.load(f)

    def read(self, key):
        if key in self.json:
            # logging.info(self.json[key])
            if self.json[key]=='true':
                return True
            elif self.json[key]=='false':
                return False
            elif is_number(self.json[key]):
                if is_int(self.json[key]):
                    return int(self.json[key])
                else:
                    return float(self.json[key])
            else:
                return self.json[key]
        else:
            logging.info(f"设置中没有这个key:{key}")
            return None

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_int(s):
    return float(s) % 1 == 0