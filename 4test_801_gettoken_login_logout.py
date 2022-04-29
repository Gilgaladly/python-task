# coding:utf-8
import logging
import time
import unittest
import ddt
import os
from common.operateRequest import sendRequest
from common.commonUtil import assert_varparam, skip_case, sleep_case
from common import operateExcel
from common.operateConfig import ConfigMethod

# 获取excel路径
curpath = os.path.dirname(os.path.realpath(__file__))
readexcelpath = os.path.join(os.path.dirname(curpath), "case")
testxlsx = os.path.join(readexcelpath, "test-801-gettoken-login-logout.xlsx")
sheetName = ["DemoYeyun"]
testdata = operateExcel.ExcelUtil(testxlsx, sheetName).dict_data()

@ddt.ddt
class Test_demo_multiExcel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.warning("执行测试用例")
        # 如果前置条件，可以写
        # 选择配置文件，每个用例都不一样，请修改 config_name 参数值, config_name="" 或者 config_name 不填，则使用默认配置文件
        cls.conf_data = ConfigMethod().config_data_method(config_name="")

    @ddt.data(*testdata)
    def test_demo(self, data):
        """"""
        # 用例中如果又转义字符的，那么断言时会有点出入，可以忽略
        flag = skip_case(data)
        if flag:
            res = sendRequest(self.conf_data).send_requests(data)
            # 进入断言模块
            assert_varparam(data, res, self.conf_data)
        else:
            self.skipTest("数据不足或者标注为跳过此列： {}".format(data))
        # 睡眠时间
        tmp = sleep_case(data)
        time.sleep(tmp)

    @classmethod
    def tearDownClass(cls):
        logging.warning("用例执行结束")
        # 如果有环境清理需要，可以写


if __name__ == "__main__":
    unittest.main()

