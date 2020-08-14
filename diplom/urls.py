"""diplom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path

from shop import views

urlpatterns = [
    path('admin/', admin.site.urls, name="admin_panel"),
    path('baseview/', views.baseview, name="baseview"),
    path('cart/', views.cart, name="cart"),
    path('smartphones/', views.smartphones, name="smartphones"),
    path('login/', views.login, name="login"),
    path('phone/', views.phone, name="phone"),
    path('', views.mainview, name="home"),
]