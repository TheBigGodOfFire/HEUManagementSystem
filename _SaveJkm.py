"""
监听键盘
扫码会触发键盘事件 将健康码存储到txt文本中
"""
import datetime
from pynput import keyboard
from os import mkdir
from _Log import Log

logger = Log().get_log()


class SaveJkm:
    """ 保存扫描的健康码 """

    def __init__(self):
        self.nowDay = datetime.datetime.now().strftime("%Y-%m-%d")
        # 监听键盘输入
        try:
            self.create_folder()
            with keyboard.Listener(on_press=self.on_press) as lsn:
                lsn.join()
        except QuitSoftware:
            raise QuitSoftware
        except Exception as e:
            logger.exception(e)

    def create_folder(self):
        """ 创建文件夹 """
        try:
            mkdir('./HealthCodes')
        except FileExistsError:
            pass
        except Exception as e:
            logger.exception(e)

    def on_press(self, key):
        # 当key不为功能按键时
        if type(key) != keyboard.Key:
            str_ = str(key)[1]  # 获取的数据有引号:'x' 取中间值
            # 将输入的数据写入到txt文本中
            with open(f'./HealthCodes/{self.nowDay}.txt', 'a') as f:
                if str_ == '}':
                    # 如果输入的为} 则换行  并退出监听
                    f.write(str_ + '\n')
                    return False
                else:
                    f.write(str_)
        elif key == keyboard.Key.esc:
            # exit()  # esc退出程序
            raise QuitSoftware


class QuitSoftware(Exception):
    def __str__(self):
        return '退出程序'


class GetJkm:
    """ 读取最后扫描的 """

    def __init__(self):
        self.nowDay = datetime.datetime.now().strftime("%Y-%m-%d")

    def get(self):
        """ 返回健康码 """
        try:
            with open(f'./HealthCodes/{self.nowDay}.txt', 'r') as f:
                lines = f.readlines()
                return lines[-1]
        except Exception as e:
            logger.exception(e)
