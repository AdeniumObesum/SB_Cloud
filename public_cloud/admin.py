#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File: auth
# @Author: Clare
# @WeChat: h1837866781
# @Datetime:18-11-18 下午2:10
# @Software: PyCharm
# @license : Copyright(C), Nanyang Institute of Technology
# Register your models here.

from django import forms
from django.contrib import admin
from SBCloudManager import settings
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from myauth.models import User
from myauth import models
from django.contrib.auth import get_user_model


# class UserCreateForm(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(
#         label='Password confirmation',
#         widget=forms.PasswordInput,
#     )
#
#     class Meta:
#         model = User
#         fields = ('name', 'email', 'phone')
#
#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(UserCreateForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
#

# # 修改用户表单
# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = User
#
#     def clean_password(self):
#         return self.initial["password"]


# 注册用户
class MyUserAdmin(UserAdmin):
    # form = UserChangeForm
    # add_form = UserCreateForm

    list_display = ('name', 'created_at', 'email', 'phone', 'is_delete', 'is_admin')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('is_admin',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password', 'avatar',)}),
        ('Personal info', {'fields': ('created_at', 'updated_at')}),
        (
            'Open token info',
            {
                'fields': ('access_token', 'refresh_token', 'expires_in')
            }
        ),
        ('Permissions', {'fields': ('is_delete', 'is_admin', 'is_active')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('name', 'email', 'phone', 'password1', 'password2'),
            }
        ),
    )
    ordering = ('created_at',)
    filter_horizontal = ()


admin.site.register(User, MyUserAdmin)
# user = models.ForeignKey(settings.AUTH_USER_MODEL)


