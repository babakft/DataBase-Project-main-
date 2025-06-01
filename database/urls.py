"""
URL configuration for database project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from tkinter.font import names

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path,include
from django.conf.urls.static import static
import os
from . import views

# def home_redirect(request):
#     """Redirect root URL to student login page"""
#     return redirect('/home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('student.urls')),
    path('expert/', include('services.urls')),
    path('home/',views.home, name='home'),
    path('api/experts/', views.get_experts_api, name='experts_api'),
    path('api/services/', views.get_services_api, name='services_api'),
    path('api/stats/', views.get_stats_api, name='stats_api'),
]
urlpatterns += static('/media/', document_root=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media'))
