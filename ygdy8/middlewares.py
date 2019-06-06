# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import user_agent
import requests

class Ygdy8_UA_Middleware(object):

    def process_request(self, request, spider):
        request.headers['User_Agent'] = user_agent.generate_user_agent()


class Ygdy8_proxy_Middleware(object):

    def __init__(self):
        self.url = 'http://188.131.212.24:5010/get/'
        self.ip_num = 0
        self.ip = ''


    def process_request(self, request, spider):
        if self.ip_num == 0 or self.ip_num >= 10:
            res = requests.get(url=self.url).content.decode()
            if not 'no' in res:
                self.ip = res
            self.ip_num = 1

        request.meta['proxy'] = 'http://' + self.ip

        self.ip_num += 1

        print('ip地址>>>',self.ip)



    def process_response(self, request, response, spider):
        return response

    # 如果返回超时错误,重新请求
    def process_exception(self, request, exception, spider):
        if isinstance(exception,TimeoutError):
            self.ip_num += 10
            return request

