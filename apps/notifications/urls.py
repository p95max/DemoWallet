from django.urls import path
from apps.notifications import views

app_name = 'notifications'

urlpatterns = [
    path('notifications/', views.notifications_list, name='notifications_list'),
]