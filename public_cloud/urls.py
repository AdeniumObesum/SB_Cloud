#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File: urls
# @Author: Clare
# @WeChat: h1837866781
# @Datetime:18-11-2 下午7:03
# @Software: PyCharm
# @license : Copyright(C), Nanyang Institute of Technology


from django.urls import path

from public_cloud.account import views as account_views
from public_cloud.resouce import views as resouce_views

urlpatterns = [
    # path('public_cloud/', include('public_cloud.urls')),
    path('create_family/', account_views.CreateFamily.as_view()),
    path('get_families/', account_views.GetFamily.as_view()),
    path('get_accounts/', account_views.GetAccount.as_view()),
    path('add_account/', account_views.AddAccount.as_view()),
    path('get_firms/', account_views.GetFirm.as_view()),
    path('get_account_detail/', account_views.GetAccountDetail.as_view()),
    path('import_host/', resouce_views.ImportHost.as_view()),
    path('get_family_firms/', resouce_views.GetFamilyFirm.as_view()),
    path('get_hosts/', resouce_views.GetHost.as_view()),
    path('stop_instance/', resouce_views.StopInstance.as_view()),
    path('start_instance/', resouce_views.StartInstance.as_view()),
    path('get_disks/', resouce_views.GetDisk.as_view()),
    path('get_snapshots/', resouce_views.GetSnapshot.as_view()),
]
