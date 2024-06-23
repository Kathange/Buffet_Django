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

# 從interface import 東西
# from ..interface import views as ve
from . import _3D_Cchart as chart
from . import _3D_Ccamera as camera

urlpatterns = [
    # html
    path('calib', views.calib, name='calib'),
    path('analysis', views.analysis, name='analysis'),
    # .py 中的 class
    path('FoodVedioFeedCalib', views.FoodVedioFeedCalib, name='FoodVedioFeedCalib'),
    path('captureCalib', camera.captureCalib, name='captureCalib'),
    path('generate_chart', chart.generate_chart, name='generate_chart'),
]
