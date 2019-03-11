from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from myauth import auth
from public_cloud import models
from public_cloud import serializers


class CreateFamilyView(APIView):
    """
    创建家族
    """
    authentication_classes = [auth.MyAuthentication]
    def dispatch(self, request, *args, **kwargs):
        return super(CreateFamilyView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        response = {
            'code': 0,
            'msg': 'success',
            'data': {}
        }
        user_id = request.data.get('user_id', '')
        user_email = request.data.get('user_email', '')
        family_name = request.data.get('family_name', '')
        if (user_id and user_email and family_name):
            has = models.Family.objects.filter(family_name=family_name)
            if (has):
                response['code'] = 1
                response['msg'] = '该家族已存在'
            else:
                family = models.Family.objects.create(
                    user_id=user_id,
                    user_email=user_email,
                    family_name=family_name
                )
                serializer = serializers.FamilySerializer(family)
                response['data']['obj'] = serializer.data
        else:
            response['code'] = 1
            response['msg'] = '输入值错误'
        return Response(response, status=status.HTTP_200_OK)


class AccountView(APIView):
    """
    录入账户
    """

    def dispatch(self, request, *args, **kwargs):
        return super(AccountView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = {
            'code': 0,
            'msg': 'success',
            'data': {}
        }
        access_key = request.data.get('access_key', '')
        secret_key = request.data.get('secret_key', '')
        app_id = request.data.get('app_id', '')
        family_id = request.data.get('family_id', '')
        firm_id = request.data.get('firm_id', '')
        if (access_key and secret_key and firm_id and family_id):
            models.AccountInfo.objects.update_or_create(access_key=access_key, defaults={
                access_key: access_key,
                firm_id: firm_id,
                secret_key: secret_key,
                app_id: app_id,
                family_id: family_id
            })
        else:
            response['code'] = 1
            response['msg'] = '值错误'

        return Response(response, status=status.HTTP_200_OK)
