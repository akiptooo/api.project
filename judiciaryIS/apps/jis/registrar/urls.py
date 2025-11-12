from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Main routes
    path('', views.dashboard_redirect, name='dashboard_redirect'),
    path('login/', views.manual_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.registrar_dashboard, name='dashboard'),
    path('assign-case/<int:case_id>/', views.assign_case_to_judge, name='assign_case'),
    path('welcome/', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    
    # User Management Routes
    path('users/', views.user_management, name='user_management'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('users/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    
    # Debug and test routes
    path('debug-auth/', views.debug_auth, name='debug_auth'),
    path('debug-templates/', views.debug_templates, name='debug_templates'),
    path('debug-urls/', views.debug_urls, name='debug_urls'),
    path('test/', views.test_page, name='test_page'),
]