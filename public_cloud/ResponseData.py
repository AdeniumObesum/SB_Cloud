#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : ResponseData.py
# @Author: Clare
# @Date  : 2019/3/14 
# @license : Copyright(C), Nanyang Institute of Technology 
# @Contact : 1837866781@qq.com 
# @Software : PyCharm
# code is far away from bugs with the god animal protecting
__pet__ = '''   
              ┏┓     ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
'''

from collections import ChainMap


class ResponseData(object):
    def __init__(self, code=0, msg='success', data={}, **kwargs):
        self.code = code
        self.msg = msg
        self.data = data
        self.kwargs = kwargs

    def response_data(self):
        data = {
            'code': self.code,
            'msg': self.msg,
            'data': self.data
        }
        new_data = ChainMap(data, self.kwargs)

        return new_data
