"""
URL configuration for learnDjango project.

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
# from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    # path(網頁路徑, views.py中的函式(class)名稱, 當我要在html或其他.py中使用所用的代稱)

    # html
    # path('buyer', views.buyer, name='buyer'),   # 這個目前沒用到，但不要刪，可能會出錯
    path('camera', views.camera, name='camera'),
    path('analysis', views.analysis, name='analysis'),
    path('cashier', views.cashier, name='cashier'),
    path('nutritionInfo', views.nutritionInfo, name='nutritionInfo'),
    path('loginData', views.loginData, name='loginData'),
    path('buyerData', views.buyerData, name='buyerData'),
    path('sellerData', views.sellerData, name='sellerData'),
    path('logUpData', views.logUpData, name='logUpData'),
    path('changePW', views.changePW, name='changePW'),
    path('about', views.about, name='about'),

    # .py 中的 class
    path('FoodVedioFeed', views.FoodVedioFeed, name='FoodVedioFeed'),
    path('WasteVedioFeed', views.WasteVedioFeed, name='WasteVedioFeed'),

    # path('img', views.img),
]

# ex. 如果我要debug cashier頁面，我可以直接輸入 http://127.0.0.1:8000/interface/cashier
