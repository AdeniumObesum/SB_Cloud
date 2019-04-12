from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from myauth import auth
from myauth import models as user_models
from myauth.models import User
from public_cloud import ResponseData


def acc_change_pwd(req):
    """
    修改密码
    :param req:
    :return:
    """
    pass


class LoginView(APIView):
    authentication_classes = []

    # authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = ResponseData.ResponseData().response_data()
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        登录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        response = ResponseData.ResponseData().response_data()

        email = request.data.get("email")  ## 邮箱登录
        password = request.data.get("password")

        user = authenticate(username=email, password=password)  # 调用 django 的认证模块进行认证
        if user:  # 判断验证是否通过
            # login(request, user)
            token = auth.get_token(user)
            user_models.UserToken.objects.update_or_create(user=user, defaults={'token': token})
            response['msg'] = '登录成功'
            user_msg = {
                'user_email': user.email,
                'username': user.name,
                'is_super': user.is_admin,
                'user_id': user.id,
                'user_token': token
            }
            response['data']['obj'] = user_msg
        else:
            response['code'] = 1
            response['msg'] = '用户名或密码错误'

        # return render(request, 'login.html')
        return Response(response, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData().response_data()
        user_token = request.data.get('user_token')
        has_user = user_models.UserToken.objects.filter(token=user_token)
        if has_user:
            has_user.delete()
            response['msg'] = '已注销'
        else:
            response['code'] = 1
            response['msg'] = '用户不存在'
        return Response(response, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData().response_data()
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        phone = request.data.get('phone', '')
        email = request.data.get('email', '')
        if username and password and phone and email:
            try:
                has = User.objects.get(email=email)
                response['code'] = 1
                response['msg'] = '该用户已存在'
            except:
                register = User.objects.create_user(name=username, email=email, phone=phone, password=password)
                response['msg'] = '创建成功'

        return Response(response, status=status.HTTP_200_OK)
