# -*- coding: utf-8 -*-
""" 配置文件操作 """
import configparser
from _Log import Log

logger = Log().get_log()
config = configparser.RawConfigParser()


class Config:
    """
    读取/修改配置文件
    path: 文件路径
    encode: 文件编码 默认为GBK
    """

    def __init__(self, path: str, encode: str = 'GBK'):
        self.file_path = path
        self.encode = encode

    def read(self, section: str, name: str) -> str:
        """ 读取配置文件 """
        try:
            config.read(self.file_path, self.encode)
            value = config[section][name]
            return value
        except Exception as e:
            logger.exception(e)
            return ''

    def write(self, section: str, name: str, value: str):
        """ 修改配置文件 """
        try:
            config.read(self.file_path, self.encode)
            config[section][name] = value
            with open(self.file_path, 'w') as f:
                config.write(f)
            f.close()
        except Exception as e:
            logger.exception(e)
