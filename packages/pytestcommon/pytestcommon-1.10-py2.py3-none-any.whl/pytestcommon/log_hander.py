import logging
from os import path


def logger_hander(log_name="root",
                  loger_level="DEBUG",
                  file_name=None,
                  stream_level="DEBUG",
                  file_level="INFO",
                  fmt="%(asctime)s-%(filename)s-%(levelname)s-%(lineno)d-%(message)s"):
    # 创建日志收集器logger
    logger = logging.getLogger(log_name)
    # 设置logger等级
    logger.setLevel(loger_level)
    # 设置输出处理器
    stream_hander = logging.StreamHandler()
    # 设置输出处理器的级别
    stream_hander.setLevel(stream_level)
    # 把输出处理器添加到收集器
    logger.addHandler(stream_hander)
    # 设置日志的格式
    fmt = logging.Formatter(fmt)
    stream_hander.setFormatter(fmt)

    if file_name:
        file_hander = logging.FileHandler(file_name, mode="w", encoding="utf-8")
        file_hander.setLevel(file_level)
        logger.addHandler(file_hander)
        file_hander.setFormatter(fmt)

    return logger


if __name__ == '__main__':
    log = logger_hander(file_name=path.join(path.join(path.dirname(path.dirname(path.abspath(__file__))), "logs"), "log.txt"))
    log.debug("debug信息")





# 方法2，log的类封装
# class LogHander:
#     def __init__(self,log_name=None, loger_level="DEBUG", file_name=None,
#                   stream_level="DEBUG", file_level="DEBUG",
#                   fmt="%(asctime)s-%(filename)s-%(levelname)s-%(lineno)d-%(message)s"):
#
#         # 创建日志收集器logger
#         logger = logging.getLogger(log_name)
#         # 设置logger等级
#         logger.setLevel(loger_level)
#         # 设置输出处理器
#         stream_hander = logging.StreamHandler()
#         # 设置输出处理器的级别
#         stream_hander.setLevel(stream_level)
#         # 把输出处理器添加到收集器
#         logger.addHandler(stream_hander)
#         # 设置日志的格式
#         fmt = logging.Formatter(fmt)
#         stream_hander.setFormatter(fmt)
#
#         if file_name:
#             file_hander = logging.FileHandler(file_name, encoding="utf-8")
#             file_hander.setLevel(file_level)
#             logger.addHandler(file_hander)
#             file_hander.setFormatter(fmt)
#
#         self.logger = logger
#
# if __name__ == '__main__':
#     log = LogHander(file_name="log.txt")
#     log.logger.debug("debug信息")


