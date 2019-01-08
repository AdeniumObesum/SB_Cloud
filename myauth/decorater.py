#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : decorater.py
# @Author: Clare
# @Date  : 2019/1/7 
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

from django.shortcuts import redirect


def auth(func):
    def inner(request, *args, **kwargs):
        p = request.session.get('user')
        if not p:
            return redirect('/login')
        return func(request, *args, **kwargs)

    return inner
