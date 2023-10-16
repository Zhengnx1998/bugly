# -*- coding: utf-8 -*-
# @Time : 2023/9/27 22:59
# @Author : Nancy_Z
# @Email : znx_969@163.com
# @File : test.py
# @Project : bugly_test
import logging
import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect, Page
import dingding
import smms
import app


class PyPage:

    def __init__(self):
        self.isOpenBrowser = False
        self.playwright = None
        self.context = None
        self.browser = None
        self.page = None
        self.isLogin = False
        self.smmss = smms.Smms()
        self.ding = dingding.DingDing()

    def login_by(self) -> None:
        if len(app.app.config['url_hash_list']) != 0:
            for hash_list in app.app.config['url_hash_list']:
                self.smmss.delete_image_url(hash_list)
            app.app.config['url_hash_list']=[]
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
        print("产品列表:",self.page.get_by_text("产品列表").count())
        if self.page.get_by_text("产品列表").count() == 0:
            app.app.logger.info("未登录，执行登录二维码操作")
            qr = self.page.frame_locator("iframe[name=\"ptlogin_iframe\"]").locator("#qr_area").locator("#qrlogin_img")
            el_attrs = qr.evaluate("el => el.getAttributeNames()")
            el_attrs = qr.evaluate("el => el.getAttributeNames()")
            for attr in el_attrs:
                print("属性：",attr, ":", qr.get_attribute(attr))
            while True:
                if qr.get_attribute("src") is not None:
                    break
            time.sleep(2)
            app.app.logger.info("上传登录二维码")
            qr.screenshot(path='./image/qr.png')
            self.smmss.get_token()
            self.smmss.upload_image('./image/qr.png')
            app.app.logger.info("发送登录二维码")
            self.ding.dingding_robot(self.smmss.image_url)
            time.sleep(10)
            # self.smmss.delete_image()
            app.app.config['url_hash_list'].append(self.smmss.hash)
            app.app.logger.info("结束二维码登录")
            self.isLogin = True
            # 登录成功
        if self.isLogin:
            app.app.logger.info("执行业务动作")
            self.select_dsjTV()
            time.sleep(5)
            app.app.logger.info("执行安卓业务动作")
            self.select_Android()
        else:
            app.app.logger.info("未登录不执行")

    # 电视家3.0
    def select_dsjTV(self):
        self.page.get_by_text("电视家3_0").click()
        time.sleep(5)
        # 判断x元素是否存在
        if self.page.get_by_label("Close", exact=True).count() > 0:
            self.page.get_by_label("Close", exact=True).click()
        self.page.pause()
        ad = self.page.locator('//*[@id="dashboard_head_tab"]').first.locator('//span[2]')
        app.app.logger.info("电视家3.0崩溃率为:%s", ad.text_content())
        # 判断崩溃率是否大于0.65
        if float(ad.text_content()) > -1:
            # 截图
            time.sleep(5)
            self.page.locator("div").filter(has_text=re.compile(r"^今天$")).nth(1).click()
            self.page.get_by_text("最近7天").click()
            time.sleep(5)
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
            self.ding.dingding_robot_text("电视家_3.0崩溃率为:", ad.text_content(), ["@15680059975", "@18791082880"],
                                          [dsj_tv_image_url, dsj_tv_bug_image_url])
            time.sleep(5)
            print(f"告警截图哈希值{dsj_tv_image_url_hash}")
            # self.smmss.delete_image_url(dsj_tv_image_url_hash)
            app.app.config['url_hash_list'].append(dsj_tv_image_url_hash)
            time.sleep(1)
            print(f"top截图哈希值{dsj_tv_bug_image_url_hash}")
            app.app.config['url_hash_list'].append(dsj_tv_bug_image_url_hash)
        else:
            app.app.logger.info("崩溃率小于0.65,不发送告警")

    def select_Android(self):
        self.page.get_by_text("电视家3_0").click()
        self.page.get_by_text("电视家随身版").click()
        time.sleep(5)
        ad = self.page.locator('//*[@id="dashboard_head_tab"]').first.locator('//span[2]')
        app.app.logger.info("电视家安卓崩溃率为:%s", ad.text_content())
        # 判断崩溃率是否大于0.30
        if float(ad.text_content()) > -1:
            # 截图
            self.page.locator("div").filter(has_text=re.compile(r"^今天$")).nth(1).click()
            self.page.get_by_text("最近7天").click()
            time.sleep(5)
            dsj_Android = self.page.locator(
                "xpath=//*[@class=\"_3QsyGr2hqAZjVh6fZnzI6t _3wcN4SQOWbN86r7emNH6FU _1PKKo_a_rrd5QsVWTXa1ax\"]").first
            dsj_Android.screenshot(path='./image/dsj_Android.png')
            self.smmss.get_token()
            self.smmss.upload_image('./image/dsj_Android.png')
            self.ding.dingding_robot_text("电视家_Android崩溃率为:", ad.text_content(), ["@18791082880"],
                                          [self.smmss.image_url])
            time.sleep(5)
            app.app.config['url_hash_list'].append(self.smmss.hash)
        else:
            app.app.logger.info("崩溃率小于0.30,不发送告警")
