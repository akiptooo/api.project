
from django.urls import path
from . import views

app_name = 'cases'

urlpatterns = [
    path('', views.CaseListView.as_view(), name='case_list'),  # Root path for case list
    path('create/', views.CaseCreateView.as_view(), name='case_create'),
    path('<int:pk>/', views.CaseDetailView.as_view(), name='case_detail'),
]