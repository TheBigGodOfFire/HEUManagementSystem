import sqlite3

conn = sqlite3.connect('data.db')
cur = conn.cursor()

# cur.execute("""create table student (
#     姓名 char primary key ,
#     学号 int,
#     身份证号 int,
#     学院 char,
#     专业 char,
#     班级 char,
#     手机号 int,
#     健康码 char,
#     核酸日期 date
# )
# """)
# cur.execute("insert into student values ('张三','21111111','132255222448456452','经济管理学院','经济贸易与外交','经贸三班','12313131313','12121212121212121212121212121212','2022/01/01')")
# cur.execute("update student set 核酸日期='2022/10/13'")
# c = cur.execute("select * from student")
# for i in c:
#     print(i)
# conn.commit()
c = cur.execute("select 学号, 姓名 from student where 学号='202860591'").fetchone()
print(c)

########################################################################################################
