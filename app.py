# -*- coding: utf-8 -*-
# @Time : 2023/9/27 22:59
# @Author : Nancy_Z
# @Email : znx_969@163.com
# @File : test.py
# @Project : bugly_test

import datetime
from flask import Flask
import PlaywrightOperate
from flask_apscheduler import APScheduler
import logconfig

app = Flask(__name__)
app.config['py_page'] = None
app.config['SCHEDULER_API_ENABLED'] = True
app.config['py_page'] = PlaywrightOperate.PyPage(app)
app.config['url_hash_list']=[]
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
# 日志
app.logger.addHandler(logconfig.getLogHandler())
# ctx = app_context()
# ctx.push()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@scheduler.task('cron', id='bugly', minute='*/10', max_instances=1, next_run_time=datetime.datetime.now())
@app.route('/login', methods=['GET', 'POST'])
def bugly_login():
    app.config['py_page'].login_by()
    return 'ok'


if __name__ == '__main__':
    app.run(threaded=False, port=9498)

