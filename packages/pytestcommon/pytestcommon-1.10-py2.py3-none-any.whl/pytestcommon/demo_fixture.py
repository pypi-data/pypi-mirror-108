import pytest

# request是系统内置的fixture，作用可以获取测试的上下文，可以获取环境的内容，可以获取参数化的参数
"""
mark标记
"""


@pytest.fixture(scope="session", params=["test", "dev"])
def login(request):
    print("先登录")
    print(request.param)
    return request.param


def setup_module():
    print("整个py文件只执行一次前置操作")


def teardown_module():
    print("整个py文件只执行一次后置操作")


def setup():
    print("前置操作，在每条用例之前都会执行")


def teardown():
    print("后置操作")


def test_project(login):
    print("{}环境登录后创建项目".format(login))


@pytest.mark.skip
def test_no(login):
    print(999)

@pytest.mark.web   # 只运行标记的web的pytest demo_fixture.py -s -m web
def test_mark(login):
    print(111)

