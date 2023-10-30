# -*- coding: utf-8 -*-
# @Time : 2023/9/27 23:37
# @Author : Nancy_Z
# @Email : znx_969@163.com
# @File : logconfig.py
# @Project : bugly_test

import os
import logging
import time
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


# log配置，实现日志自动按日期生成日志文件
def make_dir(make_dir_path):
    path = make_dir_path.strip()
    if not os.path.exists(path):
        os.makedirs(path)


def getLogHandler():
    # 日志地址
    log_dir_name = "./bugly/log/"
    # 文件名，以日期作为文件名
    log_file_name = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
    # 创建日志文件
    log_file_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)) + os.sep + log_dir_name
    make_dir(log_file_folder)
    log_file_str = log_file_folder + os.sep + log_file_name

    # 默认日志等级的设置
    logging.basicConfig(level=logging.INFO)

    # 基于文件大小分割
    # 创建日志记录器，指明日志保存路径,每个日志的大小，保存日志的上限
    # file_log_handler = RotatingFileHandler(log_file_str, maxBytes=1024 * 1024, backupCount=10, encoding='UTF-8')

    '''
    # 基于时间分割
    # 往文件里写入指定间隔时间自动生成文件的Handler
    # 实例化TimedRotatingFileHandler
    # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
    # S 秒
    # M 分
    # H 小时
    # D 天
    # 'W0'-'W6' 每星期（interval=0时代表星期一：W0）
    # midnight 每天凌晨
    '''
    file_log_time_handler = TimedRotatingFileHandler(filename=log_file_str, when='D', backupCount=10, encoding='utf-8')

    # 设置日志的格式                   发生时间    日志等级     日志信息文件名      函数名          行数        日志信息
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

    # 将日志记录器指定日志的格式
    # file_log_handler.setFormatter(formatter)
    file_log_time_handler.setFormatter(formatter)

    # 日志等级的设置
    # file_log_handler.setLevel(logging.WARNING)

    return file_log_time_handler
