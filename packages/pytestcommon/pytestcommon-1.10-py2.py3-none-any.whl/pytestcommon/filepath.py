from os import path

# 获取配置文件的路径
CONFIG_PATH = path.dirname(path.abspath(__file__))

# 获取项目的路径
ROOT_PATH = path.dirname(CONFIG_PATH)

# 获取测试用例的路径
TEST_PATH = path.join(ROOT_PATH, "tests")

# 测试报告路径
REPORT_PATH = path.join(ROOT_PATH, "reports")

# 测试数据路径
DATA_PATH = path.join(ROOT_PATH, "data")

# 日志路径
LOG_PATH = path.join(ROOT_PATH, "logs")

# 等待时间
WAIT_TIME = 20
