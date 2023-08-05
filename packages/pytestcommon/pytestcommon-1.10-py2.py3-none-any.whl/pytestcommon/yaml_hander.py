import yaml
from os import path
from pytestcommon import filepath


def read_yaml(file, encoding="utf8"):
    """读取yaml配置文件"""
    with open(file, encoding=encoding) as f:
        conf = yaml.load(f, yaml.SafeLoader)
        return conf


if __name__ == '__main__':
    file = filepath.join(filepath.CONFIG_PATH, "config.yaml")
    print(read_yaml(file))
