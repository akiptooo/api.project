from django.urls import path
from . import views

urlpatterns = [
    path('', views.judges_list_create, name='judges_dashboard'),
    path('create/', views.judges_list_create, name='judge_create'),
    path('<int:pk>/edit/', views.judge_edit, name='judge_edit'),
]
