from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def home(req):
    '''
    首页
    :param req:
    :return:
    '''
    return render(req,'layout.html')

def acc_login(request):
    '''登录'''
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)  # 调用 django 的认证模块进行认证

        if user:  # 判断验证是否通过
            login(request, user)

            next_url = request.GET.get('next', None)
            if not next_url:
                next_url = '/crm/'
            return redirect(next_url)

    return render(request, 'login.html')
    pass



def acc_logout(req):
    '''登出'''
    logout(req)
    return redirect('/login/')
    pass
