"""
查询数据库
"""
import sqlite3
from datetime import datetime


class QueryDB:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')

    def query(self, code: str):
        """ 查询 """
        cur = self.conn.cursor()
        result = cur.execute(rf"select 学号, 姓名 from student where 健康码='{code}'").fetchone()
        if result:
            self.update(code)
        return result

    def update(self, code: str):
        now_day = datetime.now().replace(microsecond=0)
        cur = self.conn.cursor()
        cur.execute(rf"update student set 扫码时间='{now_day}' where 健康码='{code}'")
        self.conn.commit()
