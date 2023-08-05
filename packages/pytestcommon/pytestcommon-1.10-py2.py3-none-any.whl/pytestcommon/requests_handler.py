import random

import requests


def request_handler(method, url, params=None, data=None, json=None, **kwargs):
    """request访问接口封装"""
    res = requests.request(method, url, params=params, data=data, json=json, **kwargs)
    try:
        return res.json()
    except Exception as e:
        print("您返回的是{}".format(e))
        raise e


if __name__ == '__main__':
    headers = {

        "Content-Type": "application/json"
    }
    url = "http://127.0.0.1:8080/member/register"
    phone = "131" + str(random.randint(10000000, 99999999))
    info = {
        "mobile_phone": phone,
        "pwd": "12345678",
        "type": "0"
    }
    """用户注册接口"""
    rh = request_handler("post", url, json=info, headers=headers)

    print(rh)

    """用户登录接口"""
    login_url = "http://127.0.0.1:8080/member/login"

    login_data = {
        "mobile_phone": rh["data"]["mobile_phone"],
        "pwd": "12345678"
    }
    login = request_handler("post", login_url, json=login_data, headers=headers)
    print(login)
