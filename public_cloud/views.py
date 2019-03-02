from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from myauth.decorater import auth
from myauth.models import User
import json


# Create your views here.

@auth
def home(req):
    '''
    首页
    :param req:
    :return:
    '''
    return render(req, 'layout.html')


def acc_login(request):
    '''登录'''
    if request.method == "POST":
        email = request.POST.get("email")  ## 邮箱登录
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)  # 调用 django 的认证模块进行认证

        if user:  # 判断验证是否通过
            login(request, user)
            request.session['user'] = email + password
            request.session.set_expiry(0)
            next_url = request.GET.get('next', None)
            if not next_url:
                next_url = '/home/'
            return redirect(next_url)

    return render(request, 'login.html')
    pass


def acc_logout(req):
    '''登出'''
    logout(req)
    req.session.clear()
    return redirect('/login/')
    pass


def acc_registe(req):
    """
    用户注册
    :param req:
    :return:
    """
    if req.method == 'GET':
        return render(req, 'registe.html')
    if req.method == 'POST':
        username = req.POST.get('username', '')
        password = req.POST.get('password', '')
        phone = req.POST.get('phone', '')
        email = req.POST.get('email', '')
        data = {
            'username': username,
            'password': password,
            'phone': phone,
            'email': email
        }
        data = json.dumps(data)
        if username and password and phone and email:
            regist = User.objects.create_user(name=username, email=email, phone=phone, password=password)
            return HttpResponse(data)

        return HttpResponse(data)