# coding:utf-8
import unittest, logging
import ddt
import os
from common.operateRequest import sendRequest
from common.commonUtil import assert_varparam,skip_case
from common import operateExcel


# 获取excel路径
curpath = os.path.dirname(os.path.realpath(__file__))
readexcelpath = os.path.join(os.path.dirname(curpath), "case")
testxlsx = os.path.join(readexcelpath, "test-yeyun.xlsx")
sheetName = ["Sheet3"]
testdata = operateExcel.ExcelUtil(testxlsx,sheetName).dict_data()


@ddt.ddt
class Test_login_community(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.warning("执行测试用例")
        # 如果前置条件，可以写

    @ddt.data(*testdata)
    def test_listinfo(self, data):
        """登录时的case """
        # 如果某一行数据空或者列表有效字段数量不够，则不执行
        flag = skip_case(data)
        if flag:
            res = sendRequest().send_requests(data)
            # 进入断言模块
            assert_varparam(data, res, self.conf_data)
        else:
            logging.info("数据不足或者标注为跳过此列： {}".format(data))
            self.skipTest("数据不足或者标注为跳过此列： {}".format(data))
        #  TODO 后续字段有变化 可以修改


    @classmethod
    def tearDownClass(cls):
        logging.warning("用例执行结束")
        # 如果有环境清理需要，可以写


if __name__ == "__main__":
    unittest.main()

