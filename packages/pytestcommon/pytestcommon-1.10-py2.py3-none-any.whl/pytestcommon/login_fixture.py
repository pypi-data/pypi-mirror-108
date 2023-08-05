# import random
#
# import pytest
# import requests
# import re
# # request是系统内置的fixture，作用可以获取测试的上下文，可以获取环境的内容，可以获取参数化的参数
# from common import requests_handler
#
#
# # @pytest.fixture(scope="session")
# # def login():
# #     url = "https://data.dmhub.cn/data/login"
# #     body = {"username": "24", "password": "Focuson789"}
# #     s = requests.session()
# #     r = s.post(url=url, data=body)
# #     re_cookies = re.findall("accessToken=(.*?) ", str(s.cookies))
# #     # print(re_cookies)
# #     url2 = "https://data.dmhub.cn/data/users/current"
# #     r2 = s.get(url2)
# #     print(r2)
# #     return re_cookies[0]
# #
#
# # def test_uers(login):
# #     url2 = "https://data.dmhub.cn/data/users/current"
# #     # heads = {"accessToken": login(), "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
# #     # print(heads)
# #     res = login.request("GET", url=url2)
# #     print(res.text)
#
#
#     def test_project_manager(self):
#         """登录"""
#         url = "https://data.dmhub.cn/data/login"
#         body = {"username": "24", "password": "Focuson789"}
#         s = requests.session()
#         r = s.post(url=url, data=body)
#         url2 = "https://data.dmhub.cn/data/users/current"
#         r2 = s.get(url2)
#
#         """创建多项目"""
#         name = random.randint(1, 9999)
#         url3 = "https://data.dmhub.cn/data/projects"
#         body3 = {
#             "name": "测试项目{}".format(name),
#             "type": "test",
#             "description": "这是一个测试项目"
#         }
#
#         re = s.post(url=url3, json=body3)
#         res_encoding = re.content.decode(re.apparent_encoding)
#         print(res_encoding)
