#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File: urls
# @Author: Clare
# @WeChat: h1837866781
# @Datetime:18-11-2 下午7:03
# @Software: PyCharm
# @license : Copyright(C), Nanyang Institute of Technology


from django.urls import path

from public_cloud.account import views

urlpatterns = [
    # path('public_cloud/', include('public_cloud.urls')),
    path('create_family/', views.CreateFamily.as_view()),
    path('get_families/', views.GetFamily.as_view()),
]
