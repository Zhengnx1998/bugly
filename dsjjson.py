import json


def json_handle(page, app):
    # 拦截get-crash-trend接口
    with page.expect_response("*get-crash-trend*", timeout=30000) as response_info:
        page.get_by_text("最近7天").click()
    response = response_info.value
    print(response.text())
    data = json.loads(response_info.value.text())["data"]["data"]
    # 创建一个空列表，用于存储计算结果
    crash_list = []
    # 循环处理每个数据
    for item in data:
        if item.get("accessUser") == -1:
            crash_list.append('0')
        else:
            crash = item.get("crashUser") / item.get("accessUser")
            crash_list.append(format(crash * 100, ".2f"))
    print("列表", crash_list)
    crash_max = max(crash_list)
    app.logger.info("7日内最大崩溃值是：%s", crash_max)
    return crash_max
