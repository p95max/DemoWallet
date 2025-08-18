from django.urls import path
from apps.accounts import views

app_name = 'wallets'

urlpatterns = [
    path('wallets/', views.wallets, name='wallets'),
    path('wallet/<int:pk>/', views.wallet_detail, name='wallet_detail'),
    path('wallets/wallets/transfer/', views.transfer_wallet_internal, name='transfer_wallet'),
    path('wallets/create/', views.create_wallet, name='create_wallet'),
    path('wallets/<int:pk>/topup/', views.topup_wallet, name='topup_wallet'),
    path('wallets/<int:pk>/delete/', views.delete_wallet, name='delete_wallet'),
    path('ajax/get_user_wallets/', views.get_user_wallets, name='get_user_wallets'),

]