"""SBCloudManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from public_cloud import views

router = routers.DefaultRouter()
# router.register('/users', views.UserViewSet)
# router.register('/blogs/', views.BlogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', get_schema_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('change_pwd/', views.acc_change_pwd),
    path('families/', views.Family.as_view()),
    # path('acc_user_menu/', views.acc_user_menu),
    path('public_cloud/', include('public_cloud.urls')),
]
