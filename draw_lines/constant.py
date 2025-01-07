import os
import toml


def read_config():
    """"读取配置"""
    file_path = f"{os.path}"
    with open(file_path) as toml_file:
        config = toml.load(toml_file)
    return config


config = read_config()
