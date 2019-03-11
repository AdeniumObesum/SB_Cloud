from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from myauth import auth
from myauth import models as user_models
from myauth.models import User
from public_cloud import models
from public_cloud import serializers


def acc_change_pwd(req):
    """
    修改密码
    :param req:
    :return:
    """
    pass


def acc_user_menu(req):
    """
    菜单
    :param req:
    :return:
    """

    pass


# class BlogViewSet(viewsets.ModelViewSet):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer
#     permission_classes = (IsOwnerOrReadOnly,)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=User.objects.get(id=self.request.session.get('user_id')))
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class LoginView(APIView):
    authentication_classes = []

    # authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = {
            'code': 0,
            'msg': 'success',
            'data': {}
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        登录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = {
            'code': 0,
            'msg': 'success',
            'data': []
        }

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


# class LogoutView(APIView):
#     def dispatch(self, request, *args, **kwargs):
#         return super(LogoutView, self).dispatch(request, *args, **kwargs)
#
#     def get(self, request, *args, **kwargs):
#         response = {
#             'code': 0,
#             'msg': 'success',
#             'data': {}
#         }
#         logout(request)
#         request.session.clear()
#         return Response(response, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = {
            'code': 0,
            'msg': 'success',
            'data': {}
        }
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        phone = request.data.get('phone', '')
        email = request.data.get('email', '')
        # data = {
        #     'username': username,
        #     'password': password,
        #     'phone': phone,
        #     'email': email
        # }
        if username and password and phone and email:
            try:
                has = User.objects.get(email=email)
                response['code'] = 1
                response['msg'] = '该用户已存在'
            except:
                register = User.objects.create_user(name=username, email=email, phone=phone, password=password)
                response['msg'] = '创建成功'

        return Response(response, status=status.HTTP_200_OK)


class Family(APIView):
    """
    家族类
    """
    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(Family, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = {
            'code': 0,
            'msg': 'success',
            'data': {}
        }
        user_id = request.data.get('user_id', '')
        if user_id:
            families = models.Family.objects.filter(user_id=user_id)
            serializer = serializers.FamilySerializer(families, many=True)
            response['data']['obj'] = serializer.data
        else:
            response['code'] = 1
            response['msg'] = '用户为空'

        return Response(response, status=status.HTTP_200_OK)
