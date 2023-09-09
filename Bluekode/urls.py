"""Bluekode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from OIS import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('billscreen/',views.ViewClass.billscreen,name='billscreen'),
    path('categorymaster/',views.ViewClass.categorymaster,name='category master'),
    path('companymaster/',views.ViewClass.companymaster,name='company master'),
    path('login/',views.ViewClass.login),
    path('productmaster/',views.ViewClass.productmaster),
    path('subcategory/',views.ViewClass.subcategory),
    path('uom/',views.ViewClass.uom),
    path('usermaster/',views.ViewClass.usermaster),
    path('',views.ViewClass.index),
    path('nav/',views.ViewClass.nav),
    path('userform',views.ViewClass.userform),
    path('userretrieve',views.ViewClass.userretrive),
    path('commasterform',views.ViewClass.commasterform),
    path('catmasterform',views.ViewClass.catmasterform),
    path('subcatform',views.ViewClass.subcatmasterform),
    path('uomform',views.ViewClass.uommasterform),
    path('prodform',views.ViewClass.prodmasterform),
    path('dashboard/',views.ViewClass.dashboardform),
    path('logout/',views.ViewClass.logout),
]
