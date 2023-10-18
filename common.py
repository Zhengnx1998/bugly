# -*- coding: utf-8 -*-
# @Time : 2023/9/27 22:59
# @Author : Nancy_Z
# @Email : znx_969@163.com
# @File : test.py
# @Project : bugly_test
import json


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
        return
    else:
        crash_list_six = crash_list[-6:]
        print("最近6小时的数据为", crash_list_six)
        crash_max = max(crash_list_six)
        app.logger.info("最近6小时内最大崩溃值是：%s", crash_max)
        return crash_max


def tool_list(hash_url, hash_list):
    if hash_url not in hash_list:
        hash_list.append(hash_url)
