from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.main_page, name='main'),
    path('dashboard/', views.dashboard_page, name='dashboard'),
    ]
