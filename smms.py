# -*- coding: utf-8 -*-
# @Time : 2023/9/27 22:59
# @Author : Nancy_Z
# @Email : znx_969@163.com
# @File : test.py
# @Project : bugly_test


import requests


class Smms:

    def __init__(self, app):
        self.image_url = None
        self.hash = None
        self.token = None
        self.url = "https://sm.ms/api/v2"
        self.username = "timetest"
        self.password = "Test123456"
        self.app = app

    def get_token(self):
        data_json = {"username": self.username, "password": self.password}
        response = requests.post(self.url + '/token', params=data_json)
        print("Token返回值：", response.json()["data"]["token"])
        self.token = response.json()["data"]["token"]
        response.close()

    def upload_image(self, file_path):
        header = {'Authorization': self.token}
        file = {"smfile": open(file_path, "rb")}
        response = requests.post(self.url + '/upload', files=file, headers=header)
        if response.status_code == 200:
            self.app.logger.info(f"{self.url},{file_path}上传成功")
            print(response.json())
            if response.json()["code"] == 'success':
                self.hash = response.json()["data"]["hash"]
                self.image_url = response.json()["data"]["url"]
            elif response.json()["code"] == 'image_repeated':
                self.image_url = response.json()["images"]

    def delete_image(self):
        if self.hash is not None:
            header = {'Authorization': self.token}
            response = requests.get(self.url + '/delete/' + self.hash, headers=header)
            if response.status_code == 200:
                self.app.logger.info(f"{self.url}删除成功")
                self.hash = None

    def delete_image_url(self, hash):
        header = {'Authorization': self.token}
        response = requests.get(self.url + '/delete/' + hash, headers=header)
        if response.status_code == 200:
            self.app.logger.info(f"{self.url}删除成功")
