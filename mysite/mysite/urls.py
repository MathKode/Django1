"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from .views import index, equipment, getData, home_test, showResult, data_upgrade, equipment_update

urlpatterns = [
    path('', index, name="Website_homepage"),
    path('formtest/',getData,name="formtest"),
    path('test/',home_test,name="test"),
    path('ShowResult/',showResult,name="showResult"),
    path('equipment/', equipment, name="equipment"),
    path('equipment_new/',data_upgrade,name="equipment_new"),
    path('equipment_update/',equipment_update,name="equipment_update"),
    path('admin/', admin.site.urls),
]
