# -*- coding: utf-8 -*-
# @Time : 2023/9/27 22:59
# @Author : Nancy_Z
# @Email : znx_969@163.com
# @File : test.py
# @Project : bugly_test
import datetime
import json
import re
import time

url = "http://47.93.62.235/buglyImage/"
path_url = "/www/wwwroot/47.93.62.235/buglyImage/"
product_dict = {"电视家3_0": ["dsj_tv_image.png", "dsj_tv_bug_image.png", "电视家TV端近6小时最高崩溃率为:"],
                "电视家随身版": ["dsj_android_image.png", "dsj_android_bug_image.png", "电视家安卓近6小时内崩溃率最高为:"]}


def json_handle(page, app, product):
    # 拦截get-crash-trend接口
    with page.expect_response("*get-real-time-hourly-stat*", timeout=30000) as response_info:
        page.get_by_text(product).click()
        page.get_by_text(product).nth(1).click()
        print("点击结束")
    response = response_info.value
    print(response.text())
    data = json.loads(response_info.value.text())["data"]["data"]
    # 创建一个空列表，用于存储计算结果
    crash_list = []
    # 循环处理每个数据
    for item in data:
        if item.get("accessUser") == 0:
            crash_list.append('0')
        else:
            crash = item.get("crashUser") / item.get("accessUser")
            crash_list.append(format(crash * 100, ".2f"))
    print("当天的数据为：", crash_list)
    if len(crash_list) < 6:
        return 0
    else:
        crash_list_six = crash_list[-6:]
        print("最近6小时的数据为", crash_list_six)
        crash_max = max(crash_list_six)
        app.logger.info("最近6小时内最大崩溃值是：%s", crash_max)
        return crash_max


def select_product(page, app, ding, product_name, now_product_name, threshold):
    if now_product_name is not None:
        page.get_by_text(now_product_name).click()
    page.get_by_text(product_name).click()
    # 判断x元素是否存在
    if page.get_by_label("Close", exact=True).count() > 0:
        page.get_by_label("Close", exact=True).click()
    max_dsj = json_handle(page, app, product_name)
    time.sleep(5)
    page.locator("div").filter(has_text=re.compile(r"^今天$")).nth(1).click()
    page.get_by_text("最近7天").click()
    # 判断崩溃率是否大于阈值或者当前时间=18点0几分
    if (datetime.datetime.now().hour == 18 and datetime.datetime.now().minute // 10 == 0) or float(
            max_dsj) > threshold:
        # 切换到7天的数据截图
        time.sleep(5)
        seven_day_image = page.locator(
            "xpath=//*[@class=\"_3QsyGr2hqAZjVh6fZnzI6t _3wcN4SQOWbN86r7emNH6FU _1PKKo_a_rrd5QsVWTXa1ax\"]").first
        seven_day_image.screenshot(path=path_url+product_dict.get(product_name)[0])
        time.sleep(5)
        # 截图top问题table
        top_bug_image = page.locator("xpath=/html/body/div/div/div/div[2]/div/div[2]/div[3]")
        top_bug_image.screenshot(path=path_url+product_dict.get(product_name)[1])

        ding.dingding_robot_text(product_dict.get(product_name)[2], str(max_dsj),
                                 ["@18780106625", "@15680059975", "@18502828246", "@15669027751"],
                                 [url+product_dict.get(product_name)[0],
                                  url+product_dict.get(product_name)[1]])
    else:
        app.logger.info(product_name+"小于"+threshold+",且没有到6点，不发送告警")
    return product_name
