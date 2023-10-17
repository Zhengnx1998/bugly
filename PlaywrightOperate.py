# -*- coding: utf-8 -*-
# @Time : 2023/9/27 22:59
# @Author : Nancy_Z
# @Email : znx_969@163.com
# @File : test.py
# @Project : bugly_test
import re
import time
from playwright.sync_api import sync_playwright
import dingding
import smms
import dsjjson


class PyPage:

    def __init__(self, app):
        self.isOpenBrowser = False
        self.playwright = None
        self.context = None
        self.browser = None
        self.page = None
        self.isLogin = False
        self.smmss = smms.Smms(app)
        self.ding = dingding.DingDing(app)
        self.app = app

    def login_by(self) -> None:
        if len(self.app.config['url_hash_list']) != 0:
            for hash_list in self.app.config['url_hash_list']:
                self.smmss.delete_image_url(hash_list)
            self.app.config['url_hash_list'] = []
        if self.isOpenBrowser is False:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=True)
            self.context = self.browser.new_context(
                viewport={'width': 2560, 'height': 1660}
            )
            page = self.context.new_page()
            self.page = page
            self.isOpenBrowser = True
        self.page.goto("https://bugly.qq.com/v2/workbench/apps")
        time.sleep(5)
        print("产品列表:", self.page.get_by_text("产品列表").count())
        if self.page.get_by_text("产品列表").count() == 0:
            self.app.logger.info("未登录，执行登录二维码操作")
            qr = self.page.frame_locator("iframe[name=\"ptlogin_iframe\"]").locator("#qr_area").locator("#qrlogin_img")
            el_attrs = qr.evaluate("el => el.getAttributeNames()")
            for attr in el_attrs:
                print("属性：", attr, ":", qr.get_attribute(attr))
            while True:
                if qr.get_attribute("src") is not None:
                    break
            time.sleep(2)
            self.app.logger.info("上传登录二维码")
            qr.screenshot(path='./image/qr.png')
            self.smmss.get_token()
            self.smmss.upload_image('./image/qr.png')
            self.app.logger.info("发送登录二维码")
            self.ding.dingding_robot(self.smmss.image_url)
            time.sleep(10)
            self.app.config['url_hash_list'].append(self.smmss.hash)
            self.app.logger.info("结束二维码登录")
            self.isLogin = True
            # 登录成功
        if self.isLogin:
            self.app.logger.info("执行电视家业务动作")
            self.select_dsj_tv()
            time.sleep(5)
            self.app.logger.info("执行安卓业务动作")
            self.select_android()
        else:
            self.app.logger.info("未登录不执行")

    # 电视家3.0
    def select_dsj_tv(self):
        self.page.get_by_text("电视家3_0").click()
        # 判断x元素是否存在
        if self.page.get_by_label("Close", exact=True).count() > 0:
            self.page.get_by_label("Close", exact=True).click()
        # 切换到7天的数据
        time.sleep(5)
        self.page.locator("div").filter(has_text=re.compile(r"^今天$")).nth(1).click()
        max_dsj_tv_crash = dsjjson.json_handle(self.page, self.app)
        # 判断崩溃率是否大于0.65
        if float(max_dsj_tv_crash) > -1:
            # 截图
            dsj_tv_image = self.page.locator(
                "xpath=//*[@class=\"_3QsyGr2hqAZjVh6fZnzI6t _3wcN4SQOWbN86r7emNH6FU _1PKKo_a_rrd5QsVWTXa1ax\"]").first
            dsj_tv_image.screenshot(path='./image/dsj_tv_image.png')
            self.smmss.get_token()
            self.smmss.upload_image('./image/dsj_tv_image.png')
            dsj_tv_image_url = self.smmss.image_url
            dsj_tv_image_url_hash = self.smmss.hash
            time.sleep(5)
            # 截图top问题table
            dsj_tv_bug_image = self.page.locator("xpath=/html/body/div/div/div/div[2]/div/div[2]/div[3]")
            dsj_tv_bug_image.screenshot(path='./image/dsj_tv_bug_image.png')
            self.smmss.get_token()
            self.smmss.upload_image('./image/dsj_tv_bug_image.png')
            dsj_tv_bug_image_url = self.smmss.image_url
            dsj_tv_bug_image_url_hash = self.smmss.hash
            self.ding.dingding_robot_text("电视家_3.07天内最高崩溃率为:", str(max_dsj_tv_crash),
                                          ["@15680059975", "@18791082880"],
                                          [dsj_tv_image_url, dsj_tv_bug_image_url])
            time.sleep(5)
            print(f"告警截图哈希值{dsj_tv_image_url_hash}")
            self.app.config['url_hash_list'].append(dsj_tv_image_url_hash)
            time.sleep(1)
            print(f"top截图哈希值{dsj_tv_bug_image_url_hash}")
            self.app.config['url_hash_list'].append(dsj_tv_bug_image_url_hash)
        else:
            self.app.logger.info("tv端崩溃率小于0.65,不发送告警")

    # 安卓业务
    def select_android(self):
        self.page.get_by_text("电视家3_0").click()
        self.page.get_by_text("电视家随身版").click()
        # 判断x元素是否存在
        if self.page.get_by_label("Close", exact=True).count() > 0:
            self.page.get_by_label("Close", exact=True).click()
        # 切换到7天的数据
        time.sleep(5)
        self.page.locator("div").filter(has_text=re.compile(r"^今天$")).nth(1).click()
        max_dsj_android = dsjjson.json_handle(self.page, self.app)
        # 判断崩溃率是否大于0.65
        if float(max_dsj_android) > -1:
            # 截图
            dsj_android_image = self.page.locator(
                "xpath=//*[@class=\"_3QsyGr2hqAZjVh6fZnzI6t _3wcN4SQOWbN86r7emNH6FU _1PKKo_a_rrd5QsVWTXa1ax\"]").first
            dsj_android_image.screenshot(path='./image/dsj_android_image.png')
            self.smmss.get_token()
            self.smmss.upload_image('./image/dsj_android_image.png')
            dsj_android_image_url = self.smmss.image_url
            dsj_android_image_url_hash = self.smmss.hash
            time.sleep(5)
            # 截图top问题table
            dsj_android_bug_image = self.page.locator("xpath=/html/body/div/div/div/div[2]/div/div[2]/div[3]")
            dsj_android_bug_image.screenshot(path='./image/dsj_android_bug_image.png')
            self.smmss.get_token()
            self.smmss.upload_image('./image/dsj_android_bug_image.png')
            dsj_android_bug_image_url = self.smmss.image_url
            dsj_android_bug_image_url_hash = self.smmss.hash
            self.ding.dingding_robot_text("电视家_Android崩溃率为:", str(max_dsj_android), ["@18791082880"],
                                          [dsj_android_image_url, dsj_android_bug_image_url])
            time.sleep(5)
            time.sleep(5)
            print(f"告警截图哈希值{dsj_android_image_url_hash}")
            self.app.config['url_hash_list'].append(dsj_android_image_url_hash)
            time.sleep(1)
            print(f"top截图哈希值{dsj_android_bug_image_url_hash}")
            self.app.config['url_hash_list'].append(dsj_android_bug_image_url_hash)
        else:
            self.app.logger.info("安卓崩溃率小于0.30,不发送告警")
