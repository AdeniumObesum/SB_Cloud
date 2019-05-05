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
from public_cloud.resouce import views as resource_views

urlpatterns = [
    # path('public_cloud/', include('public_cloud.urls')),
    path('create_family/', account_views.CreateFamily.as_view()),
    path('get_families/', account_views.GetFamily.as_view()),
    path('get_accounts/', account_views.GetAccount.as_view()),
    path('add_account/', account_views.AddAccount.as_view()),
    path('get_firms/', account_views.GetFirm.as_view()),
    path('get_account_detail/', account_views.GetAccountDetail.as_view()),
    path('import_host/', resource_views.ImportHost.as_view()),
    path('get_family_firms/', resource_views.GetFamilyFirm.as_view()),
    path('get_hosts/', resource_views.GetHost.as_view()),
    path('stop_instance/', resource_views.StopInstance.as_view()),
    path('start_instance/', resource_views.StartInstance.as_view()),
    path('get_disks/', resource_views.GetDisk.as_view()),
    path('get_snapshots/', resource_views.GetSnapshot.as_view()),
    path('delete_snapshot/', resource_views.DeleteSnapshot.as_view()),
    path('create_snapshot/', resource_views.CreateSnapshot.as_view()),
    path('rollback_snapshot/', resource_views.RollbackSnapshot.as_view()),
    path('cancel_host/', resource_views.CancelInstance.as_view()),
]
