"""
学生扫码系统（离线版本）
"""

import sys
from datetime import datetime
from threading import Thread

from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsDropShadowEffect
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication, Qt
from UiMain import Ui_Form

from _SaveJkm import SaveJkm, GetJkm, QuitSoftware
from _VoicePrompt import Reads
from _QueryDB import QueryDB
from _Log import Log


class Window(QWidget, Ui_Form):
    def __init__(self):
        # 调用GUI界面
        super(Window, self).__init__()
        self.setupUi(self)
        self.init_ui()  # 初始化界面

        self.reads = Reads  # 语音提示模块
        self.query = QueryDB().query  # 查询数据库模块
        self.logger = Log().get_log()  # 日志模块

        self.thread = MThread(self.set_ui_page)  # 监听扫码线程
        self.thread.end_signal.connect(self.run)  # 接收扫码完成信号 提交信息
        self.thread.quit_signal.connect(QCoreApplication.instance().quit)  # 按esc键 退出程序
        self.thread.start()  # 启动监听扫码线程

    def init_ui(self):
        """ 初始化界面 """
        # 关闭窗口标题栏
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 窗口设置阴影效果
        effect_shadow = QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(0, 0)  # 偏移
        effect_shadow.setBlurRadius(30)  # 阴影半径
        effect_shadow.setColor(Qt.gray)  # 阴影颜色
        self.stackedWidget.setGraphicsEffect(effect_shadow)  # 将设置套用到stackedWidget窗口中

        self.showFullScreen()  # 窗口全屏

    def read_text(self, text):
        """ 启用线程读取信息（不使用线程读取文字时，UI会卡住） """
        Thread(target=self.reads, args=(text,)).start()

    def set_ui_page(self, info=None):
        """ 设置UI上显示的信息 """
        if info:
            # 切换到扫码成功信息展示页 设置学生信息
            self.info_time.setText(str(datetime.now().replace(microsecond=0)))
            page, sid, name = 1, str(info[0]), str(info[1])
        elif info is None:
            # 切换到初始页面 清空学生信息
            page, sid, name = 0, '', ''
        else:  # info is False
            # 切换到扫描错误提示页 清空学生信息
            page, sid, name = 2, '', ''
        self.stackedWidget.setCurrentIndex(page)
        self.info_sid.setText(sid)
        self.info_name.setText(name)

    def run(self):
        """ 运行程序 """
        try:
            jkm = GetJkm().get()[11:43]  # 获取扫描的健康码
            result = self.query(jkm)  # 查询学生信息
            if result:  # 如果查询到信息
                self.set_ui_page(result)  # 切换到扫码成功信息展示页
                self.read_text(f"{str(result[1])}，扫码成功")  # 读取信息：“name，扫码成功”
            else:  # 未查询到信息
                self.set_ui_page(False)  # 切换到扫码失败提示页
                self.read_text("未查询到信息")  # 读取信息：“未查询到信息”
            self.thread.start()  # 启动监听扫码线程
        except Exception as e:
            self.logger.exception(e)


class MThread(QThread):
    """ 监听健康码线程 """
    end_signal = pyqtSignal()  # 扫码完成信号
    quit_signal = pyqtSignal()  # 退出程序信号

    def __init__(self, func):
        super(MThread, self).__init__()
        self.toggle_page = func  # 接收切换页面函数
        self.timing = 5  # 计时器 五秒未触发扫码 则切换页面

    def timer(self):
        """ 五秒未触发扫码 则切换页面到初始页 """
        while self.timing != -1:
            self.sleep(1)
            # print(self.timing)
            if not self.timing:  # timing == 0
                try:
                    self.toggle_page()  # 切换页面
                except RuntimeError:
                    exit()
            self.timing -= 1  # 减一秒
        else:
            self.timing = 5  # 计时完毕 重新计时

    def run(self):
        """ 启动线程 """
        try:
            SaveJkm()  # 监听扫码
        except QuitSoftware:  # 按esc 发送退出信号
            self.quit_signal.emit()
        else:
            if self.timing != 5:  # 扫码完毕 如果计时器计时中 则重新计时
                self.timing = 5
            else:
                Thread(target=self.timer).start()  # 计时器未在运行 开始计时
            self.end_signal.emit()  # 扫码完成 发送信号


def show_window():
    """ 启动离线版窗口 """
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    show_window()
