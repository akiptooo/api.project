"""
URL configuration for cms project.

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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='cases_home'),
    path('create/', views.case_create, name='case_create'),
    path('<int:pk>/edit/', views.case_edit, name='case_edit'),
    path('<int:pk>/', views.case_detail, name='case_detail'),
    path('search/', views.case_search, name='case_search'),
]
