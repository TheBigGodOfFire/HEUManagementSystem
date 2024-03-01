"""
学生扫码系统
"""
import time
from Main_Off_net import show_window
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By

from _VoicePrompt import Reads
from _SaveJkm import SaveJkm, GetJkm, QuitSoftware
from _ConfigFile import Config
from _Log import Log

config = Config('./config.ini').read

url = config('xpath', 'url')  # 提交信息的链接
jkmId = config('xpath', 'health code')  # 健康码
stuId = config('xpath', 'student id')  # 学号
stuName = config('xpath', 'student name')  # 学生行吗
btnOk = config('xpath', 'submit button')  # 提交按钮
sbmOk = config('xpath', 'submit ok')  # 提交成功后的姓名


class Main:
    def __init__(self):
        # 文本读取模块
        self.reads = Reads  # 语音提示模块
        self.logger = Log().get_log()  # 日志模块
        self.run()  # 运行程序

    def run(self):
        """ 运行程序 """
        option = self.set_option()
        browser = self.open_browser(option=option)
        if browser:
            while True:
                try:
                    # 检测浏览器是否被关闭
                    browser.get(url=url)
                    SaveJkm()  # 监听扫码
                    browser.execute_script('javascript:void(0);')  # 判断浏览器是否被关闭
                    self.query_info(browser=browser)  # 查询信息
                    time.sleep(1)  # 等待1秒
                except exceptions.NoSuchWindowException:
                    # 浏览器被关闭 重启浏览器
                    self.reads("正在重新启动程序")
                    browser = self.open_browser(option=option)
                except exceptions.WebDriverException:
                    # 无网络
                    self.reads("无网络连接")
                    browser.quit()
                    show_window()
                    break
                except AttributeError:
                    break
                except QuitSoftware:
                    break
                except Exception as e:
                    self.logger.exception(e)
        else:
            self.reads("未检测到“Chrome浏览器”，正在启动离线版")
            show_window()

    def query_info(self, browser, index=0, wait=1):
        """ 最多查询三次 分别等待1、2、4秒 未查询到信息则返回False """
        try:
            if index < 3:
                # 最多递归3次
                stu_name = self.submit_info(browser=browser, wait=wait)  # 等待n*2秒 点击提交
                if stu_name:
                    check = self.check_info(browser=browser, name=stu_name)
                    if check:
                        self.reads(f"{stu_name}，扫码成功")
                        return True
                self.query_info(browser, index=index + 1, wait=wait * 2)  # 查询失败 递归下一次
            else:
                # 查询3次未查询到信息 提示未查询到信息
                self.reads("未查询到信息，请重新扫码")
                return False
        except Exception as e:
            self.logger.exception(e)

    def set_option(self):
        """ 设置浏览器选项 """
        # 创建浏览器选项
        try:
            option = webdriver.ChromeOptions()
            # option.binary_location = r'F:.\WeBrowser.exe'

            # 设置浏览器全屏
            option.add_argument('-kiosk')
            # 关闭浏览器被控制通知
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            return option
        except Exception as e:
            self.logger.exception(e)

    def open_browser(self, option):
        """ 打开浏览器 """
        # 打开谷歌浏览器 应用浏览器选项
        try:
            browser = webdriver.Chrome(options=option)
            browser.implicitly_wait(3)  # 加载等待
            return browser
        except exceptions.WebDriverException:
            pass
        except Exception as e:
            self.logger.exception(e)
        return False

    def submit_info(self, browser, wait):
        """ 填写健康码 获取学生信息 提交信息 """
        try:
            jkm = GetJkm().get()  # 获取健康码
            jkm_id = browser.find_element(By.XPATH, value=jkmId)  # 健康码的input
            jkm_id.clear()  # 清除input中的内容
            jkm_id.send_keys(jkm)  # 填写健康码
            # jkm_id.click()

            stu_id = browser.find_element(By.XPATH, value=stuId)  # 学号的input
            stu_id.click()  # 点击学号的input

            time.sleep(wait)  # 等待n*2秒 获取学号等信息
            stu_id = stu_id.get_attribute('value')  # 获取学号

            if len(stu_id) != 8 or not stu_id:
                # 如果 学号长度不为8 或 学号为空
                return ''

            stu_name = browser.find_element(By.XPATH, value=stuName).text  # 获取学生姓名
            if stu_name == "暂无内容" or not stu_name:
                # 如果 姓名为"暂无内容" 或 为空
                return ''

            browser.find_element(By.XPATH, value=btnOk).click()  # 点击提交按钮

            return stu_name
        except exceptions.NoSuchElementException:
            self.logger.error('请更新配置的xpath')
        except Exception as e:
            self.logger.exception(e)

    def check_info(self, browser, name) -> bool:
        """ 检查提交成功后的信息是否正确 """
        try:
            index = 0
            while index < 50:
                # 超过10秒跳出循环
                get_name = browser.find_element(By.XPATH, value=sbmOk).text
                if get_name:
                    # 姓名不为空
                    if get_name == name:
                        # 获取到的姓名 等于 提交前的姓名
                        return True
                    break
                time.sleep(0.2)  # 每0.2秒循环一次
                index += 1
            return False
        except exceptions.NoSuchElementException:
            self.logger.error('请更新配置的xpath')
        except Exception as e:
            self.logger.exception(e)


if __name__ == '__main__':
    main = Main()
