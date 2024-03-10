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

from . import _3D_readRFID as rfid
from . import _3D_delete as del3d
from . import _3D_unetinput as ui

urlpatterns = [
    # path(網頁路徑, views.py中的函式(class)名稱, 當我要在html或其他.py中使用所用的代稱)

    # html
    path('camera', views.camera, name='camera'),
    path('cashier', views.cashier, name='cashier'),
    path('about', views.about, name='about'),
    path('joinMember', views.joinMember, name='joinMember'),
    path('negative', views.negative, name='negative'),
    # .py 中的 class
    path('gen', views.gen, name='gen'),
    path('FoodVedioFeed', views.FoodVedioFeed, name='FoodVedioFeed'),
    path('readRFID', rfid.readRFID, name='readRFID'),
    path('getUserBool', views.getUserBool, name='getUserBool'),
    path('delete', del3d.delete, name='delete'),
    path('unetinput', ui.doing, name='unetinput'),
    path('onclick', rfid.onclick, name='onclick'),
]

# ex. 如果我要debug cashier頁面，我可以直接輸入 http://127.0.0.1:8000/interface/cashier
