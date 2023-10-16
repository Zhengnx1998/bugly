# -*- coding: utf-8 -*-
# @Time : 2023/9/27 22:59
# @Author : Nancy_Z
# @Email : znx_969@163.com
# @File : test.py
# @Project : bugly_test
import time
import datetime

import requests

import app


class DingDing:

    def dingding_robot(self, image_url):
        url = 'https://oapi.dingtalk.com/robot/send?access_token=42876cced0f0b2c96af38c1849abb98425733b5beb83a53a0180dc1d3482c0d2'
        header = {'Content-Type': 'application/json'}
        json_data = {
            "markdown": {
                "title": "bugly崩溃登录",
                "text": "### bugly崩溃登录\n ![screenshot](" + image_url + ")"
            },
            "msgtype": "markdown"
        }
        response = requests.post(url, json=json_data, headers=header)
        print(response.text)

    def dingding_robot_text(self, name, text, atMobiles, image_list):
        # if int(datetime.datetime.now().strftime("%H")) % 3 == 0:
            str_mobile = ""
            for mobile in atMobiles:
                str_mobile = str_mobile + mobile
            url = 'https://oapi.dingtalk.com/robot/send?access_token=42876cced0f0b2c96af38c1849abb98425733b5beb83a53a0180dc1d3482c0d2'
            header = {'Content-Type': 'application/json'}
            if len(image_list) == 1:
                json_data = {
                    "msgtype": "markdown",
                    "markdown": {
                        "title": "bugly崩溃告警",
                        "text": "### " + name + "" + text + "\n ![screenshot](" + image_list[0] + ")\n [buglyUrl链接](https://bugly.qq.com/v2/index)\n"
                                                                                               " \n  <font color='#3C85C9'> " + str_mobile + " </font> "
                    }, "theme": "red",
                    "at": {
                        "atMobiles": atMobiles,
                        "isAtAll": False
                    }
                }
            else:
                json_data = {
                    "msgtype": "markdown",
                    "markdown": {
                        "title": "bugly崩溃告警",
                        "text": "### " + name + "" + text + "\n ![screenshot](" + image_list[
                            0] + ") \n ![screenshot](" +
                                image_list[1] + ")\n [buglyUrl链接](https://bugly.qq.com/v2/index)\n"
                                                " \n  <font color='#3C85C9'> " + str_mobile + " </font> "
                    },
                    "theme": "red",
                    "at": {
                        "atMobiles": atMobiles,
                        "isAtAll": False
                    }
                }
            response = requests.post(url, json=json_data, headers=header)
            print(response.text)
        # else:
        #     app.app.logger.info("每3小时发送一次钉钉告警")
