# !/usr/bin python3
# encoding    : utf-8 -*-
# @author     :   yanzi
# @file       :   ssh_mysql.py
# @Time       :   2021/4/25 13:35


import pymysql
from pymysql.cursors import DictCursor
from sshtunnel import SSHTunnelForwarder


class SSHMysql:
    def __init__(self, dbname):
        self.dbname = dbname
        self.server = SSHTunnelForwarder(
                ssh_address_or_host=('121.5.163.37', 10022),
                ssh_username='root',
                ssh_password='6uqJvrkbnvJDRcHg',
                remote_bind_address=('10.2.2.13', 3306))
        self.server.start()

        self.connect = pymysql.connect(
            host="127.0.0.1",
            port=self.server.local_bind_port,
            user="root",
            password="6uqJvrkbnvJDRcHg",
            cursorclass=DictCursor
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
    SQL = SSHMysql("data_t1")
    data = SQL.select_data("delete FROM data_t1.data_project where name = 'test_yanzi';")
    print(data)



