#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : auth.py
# @Author: Clare
# @Date  : 2019/3/8 
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

import hashlib
import time

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from myauth import models


class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.data.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        # 在rest framework内部会将整个两个字段赋值给request，以供后续操作使用
        return (token_obj.user, token_obj)

    def authenticate_header(self, request):
        pass


def get_token(user):
    c_time = str(time.time())
    hash_value = hashlib.md5(user.email.encode("utf-8"))
    hash_value.update(c_time.encode("utf-8"))
    return hash_value.hexdigest()
