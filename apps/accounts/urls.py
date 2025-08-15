from django.urls import path
from apps.accounts import views

app_name = 'wallets'

urlpatterns = [
    path('wallets/', views.wallets, name='wallets'),
    path('wallets/create/', views.create_wallet, name='create_wallet'),
    path('wallets/<int:pk>/delete/', views.delete_wallet, name='delete_wallet'),
]