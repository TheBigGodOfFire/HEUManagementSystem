"""
语音提示
"""

# import pyttsx3
# import pyttsx3.drivers
# import pyttsx3.drivers.sapi5
import speech
import pythoncom


class Reads:
    def __init__(self, text: str):
        pythoncom.CoInitialize()
        speech.say(text)


# class Reads:
#     def __init__(self, text: str):
#         pythoncom.CoInitialize()
#         self.engine = pyttsx3.init()
#         self.set_engine()
#         # Thread(target=self.read_text, args=(text,)).start()
#         self.read_text(text)
#
#     def set_engine(self):
#         """ 设置引擎 """
#         # 设置发音速度，默认值为200
#         self.engine.setProperty('rate', 200)
#
#         # 设置发音大小，范围为0.0-1.0
#         self.engine.setProperty('volum', 1.0)
#
#         # 设置默认声音，0是女生
#         voices = self.engine.getProperty('voices')
#         self.engine.setProperty('voice', voices[0].id)
#
#     def read_text(self, text):
#         """ 读取文本内容 """
#         try:
#             self.engine.say(text)
#             self.engine.runAndWait()
#             self.engine.stop()
#         except RuntimeError:
#             self.engine.endLoop()
#             self.read_text(text)
