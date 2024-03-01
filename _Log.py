# -*- coding: utf-8 -*-

import logging
from os import mkdir
from logging.handlers import TimedRotatingFileHandler


class Log:

    def __init__(self, level='DEBUG'):
        # 日志器对象
        self.log = logging.getLogger('log')
        self.log.setLevel(level)

    def console_handle(self, level='DEBUG'):
        """控制台处理器"""

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        # 处理器添加格式
        console_handler.setFormatter(self.get_formatter()[0])
        return console_handler

    def file_handle(self, level='DEBUG'):
        """文件处理器"""
        try:
            mkdir('./log')
        except FileExistsError:
            pass
        file_handler = TimedRotatingFileHandler('./log/INFO.log', 'midnight', 1, 3)
        file_handler.setLevel(level)
        # 处理器添加格式
        file_handler.setFormatter(self.get_formatter()[1])
        return file_handler

    def get_formatter(self):
        """格式器"""

        # 定义输出格式
        console_fmt = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)s] - %(message)s')
        file_fmt = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)s] - %(message)s')
        return console_fmt, file_fmt

    def get_log(self):
        # 日志器添加控制台处理器
        self.log.addHandler(self.console_handle())
        # 日志器添加文件处理器
        self.log.addHandler(self.file_handle())
        # 返回日志实例对象
        return self.log
