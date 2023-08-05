# !/usr/bin python3                                 
# encoding    : utf-8 -*-                            
# @author     :   yanzi                              
# @file       :   get_cookie.py
# @Time       :   2021/4/23 12:51
from pprint import pprint

import requests
import re


def get_cookies():
    url = "https://data.dmhub.cn/data/login"
    body = {"username": "24", "password": "Focuson789"}
    s = requests.session()
    r = s.post(url=url, data=body)
    # print(s.cookies)
    # print(s.headers)
    # url2 = "https://data.dmhub.cn/data/users/current"
    # r2 = s.get(url2)
    result = re.findall("accessToken=(.*?) ", str(s.cookies))
    return result[0]


if __name__ == '__main__':
    print(get_cookies())

