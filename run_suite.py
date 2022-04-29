import os, sys, logging
import time
import unittest
from common import HTMLTestRunner


def env_config():
    """
    给脚本传入的参数中指定 什么环境， 测试 TEST 生产PRO 开发DEV （没有配置）, 默认测试配置
    :return: 环境标识
    """
    try:
        env = sys.argv[1]
    except IndexError as e:
        env = "TEST"
    if env.upper() == "TEST":
        env = "TEST"
    elif env.upper() == "PRO":
        env = "PRO"
    elif env.upper() == "DEV":
        env = "DEV"
    else:
        env = "TEST"
        logging.error("环境标识传入失败，请检查,默认为 test")
    return env


def rule_config():
    """
    给脚本传入的参数中指定 跑接口自动化冒烟用例，还是 主流程接口回归用例， 冒烟用例 表示smoke， 主流程功能回归用例 表示 func ， all 表示全部
    此处过滤后， 还需要对 用例文件名 做出规范
    冒烟用例 只能跑在测试环境，否则用例需要的数据 不对，且会对线上数据造成污染
    线上 只能跑回归用例，填 2
    :return:
    """
    try:
        flag = sys.argv[2]
    except IndexError as e:
        flag = "func"
    if flag.lower() == "smoke":
        flag = "smoke"
    elif flag.lower() == "func":
        flag = "func"
    elif flag.lower() == "all":
        flag = "all"
    else:
        flag = "func"
        logging.error("测试用例标识传入失败，请检查，默认为 func")
    return flag


def configname_config():
    """
    获取配置文件 名称, 非必填，不填默认使用 data_config.ini。
    由于不同用户 可能需要的host mysql redis 地址 都不一样，因此可能有多个配置在此处获取 配置文件名称后，在 operateConfig.py中解析文件
    :return: 配置文件名称
    """
    try:
        configname = sys.argv[3]
    except IndexError as e:
        configname = "data_config.ini"
    logging.info("测试用例传入的配置文件： {}".format(configname))
    return configname


def add_case(casepath, rule="test_*.py"):
    """默认加载 主流程回归的测试用例"""
    # 定义discover方法的参数
    discover = unittest.defaultTestLoader.discover(casepath,
                                                   pattern=rule, )
    return discover


def run_case(all_case, reportpath):
    """执行所有的用例, 并把结果写入测试报告"""
    # report_name = 'report-' + now + '-result.html'
    report_name = 'report-' + '-result.html'
    htmlreport = os.path.join(reportpath, report_name)
    logging.info("测试报告生成地址：%s" % htmlreport)
    fp = open(htmlreport, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                               verbosity=2,
                                               title="测试报告",
                                               description="用例执行情况")

    # 调用add_case函数返回值
    runner.run(all_case)
    fp.close()


if __name__ == '__main__':
    now = time.strftime('%Y%m%d')
    curpath = os.path.dirname(os.path.realpath(__file__))
    # 创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Log等级总开关
    # 创建一个handler，用于写入日志
    log_path = os.path.join(curpath, "logs")
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log_name_tmp = now + '_log.txt'
    log_name = os.path.join(log_path, log_name_tmp)
    fh = logging.FileHandler(log_name, mode='w')
    fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)  # 输出到console的log等级的开关
    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # 第四步，将logger添加到handler里面
    logger.addHandler(fh)
    logger.addHandler(ch)

    logging.info('当前路径：' + curpath)
    # 定义报告名称，存放路径，报告描述
    report_path = os.path.join(curpath, "report")
    if not os.path.exists(report_path):
        os.mkdir(report_path)
    logging.info('当前报告路径：' + report_path)
    case_path = os.path.join(curpath, "casefile")
    logging.info('当前用例py文件路径：' + case_path)
    env_flag = env_config()
    rule_flag = rule_config()
    # 线上环境 只能跑 主流程回归用例， 用例执行文件以 test_func_ 打头
    # 测试环境都可以选择
    # 冒烟用例执行文件以 test_smoke_ 打头
    if env_flag == "PRO":
        logging.warning("生产环境只能跑主流程回归用例，如有需要请修改代码")
        rule = "test_func_*.py"
    elif env_flag == "TEST":
        if rule_flag == "smoke":
            rule = "test_smoke_*.py"
        elif rule_flag == "func":
            rule = "test_func_*.py"
        elif rule_flag == "all":
            rule = "test_*.py"
        else:
            logging.error("测试用例选择类型出错, 请检查")
    elif env_flag == "DEV":
        rule = "test_*.py"
    logging.info("测试环境为：{} ,测试用例类型为：{}, rule: {}".format(env_flag,rule_flag, rule))
    cases = add_case(case_path, rule)
    run_case(cases, report_path)
