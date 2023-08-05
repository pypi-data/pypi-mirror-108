# encoding  : utf-8 -*-
# @author   : yanzi
# @time     : 2021/5/31 15:51
# from pymysql.cursors import DictCursor
# from os import path
from pytestcommon import mysql_handler, yaml_hander, excel_hander, log_hander, requests_handler, ssh_mysql, filepath, conftest

# def ssh_db():
#     SQL = ssh_mysql.SSHMysql("data_t1")
#     data = SQL.select_data("delete FROM data_t1.data_project where name = 'test_yanzi';")
#     print(data)
#
#
# class MysqlMid(mysql_handler.MySQLHandler):
#     """读取配置文件的选项 mysql_handler"""
#
#     def __init__(self):
#         """初始化所有的配置项，从yaml文件中读取"""
#         db_conf = MidHandler.yaml["MYSQL"]
#         super().__init__(
#             host=db_conf["host"],
#             port=db_conf["port"],
#             user=db_conf["user"],
#             password=db_conf["password"],
#             charset=db_conf["charset"],
#             cursorclass=DictCursor
#         )
#
#
# class MidHandler:
#     """初始化所有的数据，这些数据可以在其它模块中重复使用，这些模块必须从common当中实例化对象"""
#
#     # 加载Python配置项
#     conf = config
#
#     # yaml数据
#     yaml = yaml_hander.read_yaml(path.join(config.CONFIG_PATH, "config.yaml"))
#
#     # excel数据
#     __excel_path = conf.DATA_PATH
#     __excel_file = yaml["excel"]["file_path"]
#     excel = excel_hander.ExcelHandler(path.join(__excel_path, __excel_file))
#
#     # logger
#     __logger_conf = yaml["log"]
#     logger = log_hander.logger_hander(
#         log_name=__logger_conf["log_name"],
#         loger_level=__logger_conf["loger_level"],
#         file_name=path.join(conf.LOG_PATH, __logger_conf["file_name"]),
#         stream_level=__logger_conf["stream_level"],
#         file_level=__logger_conf["file_level"],
#     )
#     db_class = MysqlMid
#
#
# if __name__ == '__main__':
#     # data_path = MidHandler.conf.DATA_PATH
#     # db = MysqlMid()
#     # data = db.select_data("select * from futureloan.member limit 10;")
#     # print(data)
#     # print(MidHandler.yaml["excel"]["file_path"])
#     # print(MidHandler.logger)
#     # 测试登录
#     pass
