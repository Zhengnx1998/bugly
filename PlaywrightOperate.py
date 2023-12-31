# -*- coding: utf-8 -*-
# @Time : 2023/9/27 22:59
# @Author : Nancy_Z
# @Email : znx_969@163.com
# @File : test.py
# @Project : bugly_test

import json
import os.path
import time
from datetime import datetime

from fake_useragent import UserAgent
from playwright.sync_api import sync_playwright

import common
import dingding


class PyPage:

    def __init__(self, app):
        self.isOpenBrowser = False
        self.playwright = None
        self.context = None
        self.browser = None
        self.page = None
        self.isLogin = True
        self.ding = dingding.DingDing(app)
        self.app = app

    def init_count(self):
        if datetime.now().hour == 1 and datetime.now().minute // 10 == 0:
            file_count = open("count.json", 'w')
            file_count.write(json.dumps(common.json_dict))
            file_count.close()
            self.app.logger.info("初始化产品预警次数")
        else:
            self.app.logger.info("未到1点不初始化json文件")

    def login_by(self) -> None:
        self.init_count()
        with sync_playwright() as self.playwright:
            self.browser = self.playwright.chromium.launch(headless=True)
            if os.path.exists("state.json"):
                self.context = self.browser.new_context(storage_state="state.json",
                                                        viewport={'width': 2560, 'height': 1660}, locale="zh_CN.utf8",
                                                        user_agent=UserAgent().chrome)
            else:
                self.context = self.browser.new_context(
                    viewport={'width': 2560, 'height': 1660}, locale="zh_CN.utf8"
                )
            page = self.context.new_page()
            self.page = page
            self.isOpenBrowser = True
            self.page.goto("https://bugly.qq.com/v2/workbench/apps")
            time.sleep(5)
            print("产品列表:", self.page.get_by_text("产品列表").count())
            if self.page.get_by_text("产品列表").count() == 0:
                time.sleep(15)
                self.app.logger.info("未登录，执行登录二维码操作")
                qr = self.page.frame_locator("iframe[name=\"ptlogin_iframe\"]").locator("#qr_area").locator(
                    "#qrlogin_img")
                el_attrs = qr.evaluate("el => el.getAttributeNames()")
                for attr in el_attrs:
                    print("属性：", attr, ":", qr.get_attribute(attr))
                while True:
                    if qr.get_attribute("src") is not None:
                        break
                time.sleep(2)
                self.app.logger.info("上传登录二维码")
                qr.screenshot(path='/www/wwwroot/47.93.62.235/buglyImage/qr.png')
                self.app.logger.info("发送登录二维码")
                self.ding.dingding_robot(
                    "http://47.93.62.235/buglyImage/qr.png" + "?" + str(datetime.now().timestamp()))
                self.app.logger.info("结束二维码登录")
                self.isLogin = True
                # 登录成功
            if self.isLogin:
                now_product_name = None
                self.app.logger.info("执行电视家业务动作")
                now_product_name = common.select_product(self.page, self.app, self.ding, "电视家3_0", now_product_name,
                                                         0.65)
                print("now_product_name", now_product_name)
                time.sleep(5)
                self.app.logger.info("执行安卓业务动作")
                now_product_name = common.select_product(self.page, self.app, self.ding, "电视家随身版",
                                                         now_product_name,
                                                         0.30)
                print("now_product_name", now_product_name)
                time.sleep(5)
                self.app.logger.info("执行ios业务动作")
                now_product_name = common.select_product(self.page, self.app, self.ding, "电视家_iOS", now_product_name,
                                                         5.0)
                time.sleep(5)
                self.app.logger.info("执行火星业务动作")
                common.select_product(self.page, self.app, self.ding, "Tvmars", now_product_name,
                                      0.60)
                self.context.storage_state(path="state.json")
            else:
                self.app.logger.info("未登录不执行")

    # 电视家3.0
    # def select_dsj_tv(self):
    #     self.page.get_by_text("电视家3_0").click()
    #     # 判断x元素是否存在
    #     if self.page.get_by_label("Close", exact=True).count() > 0:
    #         self.page.get_by_label("Close", exact=True).click()
    #     # 切换到7天的数据
    #     max_dsj_tv_crash = common.json_handle(self.page, self.app, "电视家3_0")
    #     self.page.locator("div").filter(has_text=re.compile(r"^今天$")).nth(1).click()
    #     self.page.get_by_text("最近7天").click()
    #     # 判断崩溃率是否大于0.65或者当前时间=18点0几分
    #     if (datetime.datetime.now().hour == 18 and datetime.datetime.now().minute // 10 == 0) or float(
    #             max_dsj_tv_crash) > 0.65:
    #         # 截图
    #         time.sleep(5)
    #         dsj_tv_image = self.page.locator(
    #             "xpath=//*[@class=\"_3QsyGr2hqAZjVh6fZnzI6t _3wcN4SQOWbN86r7emNH6FU _1PKKo_a_rrd5QsVWTXa1ax\"]").first
    #         dsj_tv_image.screenshot(path='./image/dsj_tv_image.png')
    #         self.smmss.get_token()
    #         self.smmss.upload_image('./image/dsj_tv_image.png')
    #         dsj_tv_image_url = self.smmss.image_url
    #         dsj_tv_image_url_hash = self.smmss.hash
    #         time.sleep(5)
    #         # 截图top问题table
    #         dsj_tv_bug_image = self.page.locator("xpath=/html/body/div/div/div/div[2]/div/div[2]/div[3]")
    #         dsj_tv_bug_image.screenshot(path='./image/dsj_tv_bug_image.png')
    #         self.smmss.get_token()
    #         self.smmss.upload_image('./image/dsj_tv_bug_image.png')
    #         dsj_tv_bug_image_url = self.smmss.image_url
    #         dsj_tv_bug_image_url_hash = self.smmss.hash
    #         self.ding.dingding_robot_text("电视家TV端近6小时最高崩溃率为:", str(max_dsj_tv_crash),
    #                                       ["@18780106625", "@13618035171", "@18380473531", "@19138982495",
    #                                        "@15360584721"],
    #                                       [dsj_tv_image_url, dsj_tv_bug_image_url])
    #         time.sleep(5)
    #         print(f"告警截图哈希值{dsj_tv_image_url_hash}")
    #         common.tool_list(dsj_tv_image_url_hash, self.app.config['url_hash_list'])
    #         time.sleep(1)
    #         print(f"top截图哈希值{dsj_tv_bug_image_url_hash}")
    #         common.tool_list(dsj_tv_bug_image_url_hash, self.app.config['url_hash_list'])
    #     else:
    #         self.app.logger.info("tv端崩溃率小于0.65,且没有到6点不发送告警")
    #
    # # 安卓业务
    # def select_android(self):
    #     self.page.get_by_text("电视家3_0").click()
    #     self.page.get_by_text("电视家随身版").click()
    #     # 判断x元素是否存在
    #     if self.page.get_by_label("Close", exact=True).count() > 0:
    #         self.page.get_by_label("Close", exact=True).click()
    #     max_dsj_android = common.json_handle(self.page, self.app, "电视家随身版")
    #     time.sleep(5)
    #     self.page.locator("div").filter(has_text=re.compile(r"^今天$")).nth(1).click()
    #     self.page.get_by_text("最近7天").click()
    #     # 判断崩溃率是否大于0.30或者当前时间=18点0几分
    #     if (datetime.datetime.now().hour == 18 and datetime.datetime.now().minute // 10 == 0) or float(
    #             max_dsj_android) > 0.30:
    #         # 切换到7天的数据截图
    #         time.sleep(5)
    #         dsj_android_image = self.page.locator(
    #             "xpath=//*[@class=\"_3QsyGr2hqAZjVh6fZnzI6t _3wcN4SQOWbN86r7emNH6FU _1PKKo_a_rrd5QsVWTXa1ax\"]").first
    #         dsj_android_image.screenshot(path='./image/dsj_android_image.png')
    #         self.smmss.get_token()
    #         self.smmss.upload_image('./image/dsj_android_image.png')
    #         dsj_android_image_url = self.smmss.image_url
    #         dsj_android_image_url_hash = self.smmss.hash
    #         time.sleep(5)
    #         # 截图top问题table
    #         dsj_android_bug_image = self.page.locator("xpath=/html/body/div/div/div/div[2]/div/div[2]/div[3]")
    #         dsj_android_bug_image.screenshot(path='./image/dsj_android_bug_image.png')
    #         self.smmss.get_token()
    #         self.smmss.upload_image('./image/dsj_android_bug_image.png')
    #         dsj_android_bug_image_url = self.smmss.image_url
    #         dsj_android_bug_image_url_hash = self.smmss.hash
    #         self.ding.dingding_robot_text("电视家安卓近6小时内崩溃率最高为:", str(max_dsj_android),
    #                                       ["@18780106625", "@15680059975", "@18502828246", "@15669027751"],
    #                                       [dsj_android_image_url, dsj_android_bug_image_url])
    #         time.sleep(5)
    #         time.sleep(5)
    #         print(f"告警截图哈希值{dsj_android_image_url_hash}")
    #         # self.app.config['url_hash_list'].append(dsj_android_image_url_hash)
    #         common.tool_list(dsj_android_image_url_hash, self.app.config['url_hash_list'])
    #         time.sleep(1)
    #         print(f"top截图哈希值{dsj_android_bug_image_url_hash}")
    #         # self.app.config['url_hash_list'].append(dsj_android_bug_image_url_hash)
    #         common.tool_list(dsj_android_bug_image_url_hash, self.app.config['url_hash_list'])
    #     else:
    #         self.app.logger.info("安卓崩溃率小于0.30,且没有到6点，不发送告警")
