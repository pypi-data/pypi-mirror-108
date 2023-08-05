#封装mysql

import pymysql
from pymysql.cursors import DictCursor


class MySQLHandler:
    def __init__(self,
                 host=None,
                 port=3306,
                 user=None,
                 password=None,
                 charset="utf8",
                 cursorclass=DictCursor
                 ):
        self.connect = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset=charset,
            cursorclass=cursorclass
        )
        self.cursor = self.connect.cursor()

    def select_data(self, sql, one=True):
        """执行查询"""
        self.cursor.execute(sql)
        self.connect.commit()

        if one:
            return self.cursor.fetchone()
        return self.cursor.fetchall()

    def close_connct(self):
        """关闭数据库游标"""
        self.cursor.close()
        self.connect.close()


if __name__ == '__main__':
    SQL = MySQLHandler(
        host="121.5.163.37",
        port=10022,
        user="root",
        password="6uqJvrkbnvJDRcHg",
        charset="utf8",
        cursorclass=DictCursor
    )

    data = SQL.select_data("select * from data_t1.data_project;")
    print(data)
