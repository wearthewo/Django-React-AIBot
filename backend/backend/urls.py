"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from aibot.views import CreateUserView
from aibot.views import CustomTokenObtainPairView, CustomTokenRefreshView, MessageListCreateView, check_auth, logout

urlpatterns = [
    path("admin/", admin.site.urls), 
    path("api/user/register/", CreateUserView.as_view(), name="create_user"),
    path("api/user/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/user/token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("api/user/messages/", MessageListCreateView.as_view(), name="message_list_create"), 
    path("api/user/check-auth/", check_auth, name="check_auth"),
    path("api/user/logout/", logout, name="logout"),
    
]
