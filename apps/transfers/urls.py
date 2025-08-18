from django.urls import path
from . import views

app_name = 'transfers'

urlpatterns = [
    path('send/', views.send_transfer, name='send_transfer'),
]