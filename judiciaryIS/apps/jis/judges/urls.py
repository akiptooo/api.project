from django.urls import path
from . import views

app_name = 'judges'

urlpatterns = [
    path('dashboard/', views.judge_dashboard, name='dashboard'),
]