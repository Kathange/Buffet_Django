"""
URL configuration for buffetProject project.

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
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language
from django.conf.urls.i18n import i18n_patterns

# 在名為 buffetProject 的Project中加入url連結，這樣系統才不會找不到路徑
urlpatterns = []

urlpatterns += i18n_patterns(
    # 加上url連結
    # path('interface/', include('interface.urls')),
    # 加上管理員頁面的連結
    path('admin/', admin.site.urls),
    
    # 加上login, logout的連結(目前未用到)
    # path('accounts/', include('django.contrib.auth.urls')),

    # 設定語言
    # path('i18n/', set_language, name='set_language'),
    path('i18n/', include('django.conf.urls.i18n')),

    # 加上home連結(means當進到網路頁面之後，會直接出現home.html的內容，原本是預設空白頁面)
    path('', TemplateView.as_view(template_name = 'home.html')),

    path('interface/', include('interface.urls')),
    path('calibration/', include('calibration.urls')),
    path('waste/', include('waste.urls')),
    # prefix_default_language=False,
)

# 除了settings.py中要設定，這邊也要加上static路徑，系統才會知道(固定語法，可以不用管)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

