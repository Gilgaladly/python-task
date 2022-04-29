# coding:utf-8
import logging
import time
import unittest
import ddt
import os
from common.operateRequest import sendRequest
from common.commonUtil import assert_varparam, skip_case, sleep_case, execute_sql, execute_shell
from common import operateExcel
from common.operateConfig import ConfigMethod


# 获取excel路径
curpath = os.path.dirname(os.path.realpath(__file__))
readexcelpath = os.path.join(os.path.dirname(curpath), "case")
testxlsx = os.path.join(readexcelpath, "test-yeyun2.xlsx")
sheetName = ["DemoYeyun","sheet2","sheet3"]
testdata = operateExcel.ExcelUtil(testxlsx, sheetName).dict_data()

@ddt.ddt
class Test_demo_multiExcel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.warning("执行测试用例")
        # 如果前置条件，可以写
        # 选择配置文件，每个用例都不一样，请修改 config_name 参数值, config_name="" 或者 config_name 不填，则使用默认配置文件
        cls.conf_data = ConfigMethod().config_data_method(config_name="data_config_zhouxy.ini")


    @ddt.data(*testdata)
    def test_demo(self, data):
        """demo 多个excel情况 """
        #  TODO 后续有变化 可以修改
        flag = skip_case(data)
        if flag:
            execute_sql(data, self.conf_data)
            execute_shell(data, self.conf_data)
            res = sendRequest(self.conf_data).send_requests(data)
            # 睡眠时间
            tmp = sleep_case(data)
            time.sleep(tmp)
            # 进入断言模块
            assert_varparam(data, res, self.conf_data)
        else:
            self.skipTest("数据不足或者标注为跳过此列： {}".format(data))

    @classmethod
    def tearDownClass(cls):
        logging.warning("用例执行结束")
        # 如果有环境清理需要，可以写


if __name__ == "__main__":
    unittest.main()

