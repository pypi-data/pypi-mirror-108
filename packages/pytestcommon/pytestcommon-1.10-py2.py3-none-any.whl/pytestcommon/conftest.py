# !/usr/bin python3                                 
# encoding    : utf-8 -*-                            
# @author     :   yanzi                              
# @file       :   conftest.py
# @Time       :   2021/4/23 11:09
import pytest
from datetime import datetime
import requests
import base64
from Crypto.Cipher import AES


@pytest.fixture(scope="session")
def login_setup(url="https://data.dmhub.cn/data/index.html"):
    """前置操作先登录"""
    s = requests.session()
    body = {"username": "24", "password": "Focuson789"}
    r = s.post(url, data=body)
    return s


# @pytest.fixture(scope="session")
# def get_cookies():
#     s = requests.session()
#     return s
#
#
# @pytest.fixture(scope="session")
# def login_fix(get_cookies):
#     url = host + "/login"
#     body = {"username": "24", "password": "Focuson789"}
#     r = get_cookies.post(url, data=body)
#     return r


@pytest.fixture(scope="session")
def get_uers(get_cookies, login):
    login
    url2 = "https://data.dmhub.cn/data/users/current"
    r = get_cookies.get(url2)
    return r.json()


@pytest.fixture(scope="session")
def accessKey_Encrypt():
    url = "http://atf.xsio.cn/api/TestMock/getSignature/vsQphwtkO0K1twVh/t7bVakg2dxTUiTfG"
    res = requests.get(url).json()["signature"]
    return res
    # vi = '0102030405060708'
    # pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
    # data = pad("123456{}".format(datetime.now().strftime("%Y%m%d%H%M%S%s")))
    # # 字符串补位
    # cipher = AES.new("7Ke6FM1kOMkdjUSp".encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    # encryptedbytes = cipher.encrypt(data.encode('utf8'))
    # # 加密后得到的是bytes类型的数据
    # encodestrs = base64.b64encode(encryptedbytes)
    # # 使用Base64进行编码,返回byte字符串
    # enctext = encodestrs.decode('utf8')
    # # 对byte字符串按utf-8进行解码
    # return enctext


@pytest.fixture(scope="session")
def secretKey_Encrypt():
    vi = '0102030405060708'
    pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
    data = pad("123456{}".format(1620381818061))
    # 字符串补位
    cipher = AES.new("11fwZGtqlBrpMIMf".encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    encryptedbytes = cipher.encrypt(data.encode('utf8'))
    # 加密后得到的是bytes类型的数据
    encodestrs = base64.b64encode(encryptedbytes)
    # 使用Base64进行编码,返回byte字符串
    enctext = encodestrs.decode('utf8')
    # 对byte字符串按utf-8进行解码
    return enctext


result = {}


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    print('----------------------------')

    # 获取钩子方法的调用结果
    out = yield
    print('用例执行结果', out)

    # 3. 从钩子方法的调用结果中获取测试报告
    report = out.get_result()
    if report.when == "call":
        result[report.nodeid] = report.outcome
        print(result)
        url = "http://atf.xsio.cn/api/TestMock/getSignature/vsQphwtkO0K1twVh/t7bVakg2dxTUiTfG"
        res = requests.get(url).json()["signature"]

        url = "http://atf.xsio.cn/api/cap/sendStatus"
        body = {
            "testName": str(item.function.__doc__),
            "planid": "b8ed4654-3eae-4bf9-bf66-0375e34b2028",
            "status": "Pass"
        }
        res2 = requests.post(url=url, json=body,
                             headers={"signature": res, "accessKey": "vsQphwtkO0K1twVh"})
        print("请求参数是", body)
        print("测试结果是：", res2.text)
        print('测试报告：%s' % report)
        print('步骤：%s' % report.when)
        print('nodeid：%s' % report.nodeid)
        print('description:%s' % str(item.function.__doc__))
        print(('运行结果: %s' % report.outcome))


@pytest.fixture(scope="session", autouse=True)
def fix_a(accessKey_Encrypt):
    print("setup 前置操作")
    url = "http://atf.xsio.cn/api/cap/getData/CDP2/2e8a8291-4a14-4518-823a-6d2e88633b21"
    res = requests.get(url=url, headers={"signature": accessKey_Encrypt, "accessKey": "vsQphwtkO0K1twVh"})
    dict1 = {}
    for i in res.json():
        if i.get("name") and i.get("value"):
            dict1[i["name"]] = i["value"]
    print(dict1)
    # os.environ['password']='Focuson789'

    yield
    print("teardown 后置操作")
    # url = "http://atf.xsio.cn/api/cap/sendStatus"
    # body = {
    #     "testName": "登录成功",
    #     "planid": "b8ed4654-3eae-4bf9-bf66-0375e34b2028",
    #     "status": "PASS"
    # }
    # res = requests.post(url=url, json=body, headers={"signature": accessKey_Encrypt, "accessKey": "vsQphwtkO0K1twVh"})
    # print(res.json())
