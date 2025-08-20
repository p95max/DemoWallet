from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('all_transactions/', views.all_transactions, name='all_transactions'),
    path('<int:pk>/', views.transaction_detail, name='transaction_detail'),

    ]
