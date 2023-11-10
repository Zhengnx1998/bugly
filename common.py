# -*- coding: utf-8 -*-
# @Time : 2023/9/27 22:59
# @Author : Nancy_Z
# @Email : znx_969@163.com
# @File : test.py
# @Project : bugly_test
import json
import os
import re
import time
from datetime import datetime

url = "http://47.93.62.235/buglyImage/"
path_url = "/www/wwwroot/47.93.62.235/buglyImage/"
product_dict = {"电视家3_0": ["dsj_tv_image.png", "dsj_tv_bug_image.png", "电视家TV端版6小时内崩溃率最高为:"],
                "电视家随身版": ["dsj_android_image.png", "dsj_android_bug_image.png",
                                 "电视家Android版6小时内崩溃率最高为:"],
                "电视家_iOS": ["dsj_ios_image.png", "dsj_ios_bug_image.png", "电视家移动端ios版6小时内崩溃率最高为:"],
                "Tvmars": ["dsj_huoxing_image.png", "dsj_huoxing_bug_image.png",
                           "火星6小时内崩溃率最高为:"]}
tel_dict = {"电视家3_0": ["@18780106625", "@13618035171", "@18380473531", "@19138982495", "@15360584721"],
            "电视家随身版": ["@18780106625", "@15680059975", "@18502828246", "@15669027751"],
            "电视家_iOS": ["@18780106625", "@13076017340", "@18791082880"],
            "Tvmars": ["@18380473531", "@18780106625"]
            }
json_dict = {"电视家3_0": 0, "电视家随身版": 0, "电视家_iOS": 0, "Tvmars": 0}


def json_handle(page, app, product):
    page.get_by_text(product).click()
    page.get_by_text(product).nth(1).click()
    # 拦截get-crash-trend接口
    with page.expect_response("*get-app-real-time-trend*dataType=realTimeTrendData*", timeout=30000) as response_info:
        page.locator("span").filter(has_text="累计").locator("label").click()
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


# 检查每天发送次数
def check_count(product_name):
    # 初始化文件
    if os.path.exists("count.json") is False:
        file_count = open("count.json", 'w')
        file_count.write(json.dumps(json_dict))
        file_count.close()
    with open("count.json", 'r') as file:
        content = file.read()
    if content is None:
        filew = open("count.json", 'w')
        filew.write(json.dumps(json_dict))
        filew.close()
        content_json = json_dict
    else:
        content_json = json.loads(content)
    count = content_json[product_name]
    if count == 10:
        return True
    else:
        new_count = count + 1
        content_json[product_name] = new_count
    with open("count.json", 'w') as file:
        file.write(json.dumps(content_json))
        return False


# 查询产品线
def select_product(page, app, ding, product_name, now_product_name, threshold):
    if now_product_name is not None:
        page.get_by_text(now_product_name).click()
    page.get_by_text(product_name).click()
    # 判断x元素是否存在
    if page.get_by_label("Close", exact=True).count() > 0:
        page.get_by_label("Close", exact=True).click()
    time.sleep(5)
    max_dsj = json_handle(page, app, product_name)
    time.sleep(5)
    page.locator("div").filter(has_text=re.compile(r"^今天$")).nth(1).click()
    page.get_by_text("最近7天").click()
    # 判断崩溃率是否大于阈值或者当前时间=18点0几分
    if float(max_dsj) > threshold:
        # 切换到7天的数据截图
        time.sleep(5)
        app.logger.info("开始截图7天的数据,当前产品线为：%s", product_name)
        seven_day_image = page.locator(
            "xpath=//*[@class=\"_3QsyGr2hqAZjVh6fZnzI6t _3wcN4SQOWbN86r7emNH6FU _1PKKo_a_rrd5QsVWTXa1ax\"]").first
        seven_day_image.screenshot(path=path_url + product_dict.get(product_name)[0])
        time.sleep(5)
        # 截图top问题table
        app.logger.info("开始截图top问题的数据,当前产品为：%s", product_name)
        top_bug_image = page.locator("xpath=/html/body/div/div/div/div[2]/div/div[2]/div[3]")
        top_bug_image.screenshot(path=path_url + product_dict.get(product_name)[1])
        # 发送钉钉
        if check_count(product_name) is False:
            app.logger.info("当天%s达到告警阈值且发送次数没有达到10", product_name)
            app.logger.info("%s达到阈值%s，即将发送钉钉告警", product_name, threshold)
            ding.dingding_robot_text(product_dict.get(product_name)[2], str(max_dsj), tel_dict.get(product_name),
                                     [url + product_dict.get(product_name)[0] + "?" + str(datetime.now().timestamp()),
                                      url + product_dict.get(product_name)[1] + "?" + str(datetime.now().timestamp())])
            print(url + product_dict.get(product_name)[0] + "?" + str(datetime.now().timestamp()))
            print(url + product_dict.get(product_name)[1] + "?" + str(datetime.now().timestamp()))
        else:
            app.logger.info("当天该产品%s已发送次数达到10", product_name)
        # 判断是否当天发送次数达到10
    elif datetime.now().hour == 18 and datetime.now().minute // 10 == 0:
        app.logger.info("达到每天定点发送时间18:00")
        # 切换到7天的数据截图
        time.sleep(5)
        app.logger.info("开始截图7天的数据,当前产品线为：%s", product_name)
        seven_day_image = page.locator(
            "xpath=//*[@class=\"_3QsyGr2hqAZjVh6fZnzI6t _3wcN4SQOWbN86r7emNH6FU _1PKKo_a_rrd5QsVWTXa1ax\"]").first
        seven_day_image.screenshot(path=path_url + product_dict.get(product_name)[0])
        time.sleep(5)
        # 截图top问题table
        app.logger.info("开始截图top问题的数据,当前产品为：%s", product_name)
        top_bug_image = page.locator("xpath=/html/body/div/div/div/div[2]/div/div[2]/div[3]")
        top_bug_image.screenshot(path=path_url + product_dict.get(product_name)[1])
        # 发送钉钉
        app.logger.info("%s每天告警时间18:00，即将发送钉钉告警", product_name)
        ding.dingding_robot_text(product_dict.get(product_name)[2], str(max_dsj), None,
                                 [url + product_dict.get(product_name)[0] + "?" + str(datetime.now().timestamp()),
                                  url + product_dict.get(product_name)[1] + "?" + str(datetime.now().timestamp())])
        print(url + product_dict.get(product_name)[0] + "?" + str(datetime.now().timestamp()))
        print(url + product_dict.get(product_name)[1] + "?" + str(datetime.now().timestamp()))
    else:
        app.logger.info("%s小于%s,且没有到定点发送时间", product_name, threshold)
    return product_name
