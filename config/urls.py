from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.accounts.urls')),
    path('api/', include('apps.transactions.urls')),
    path('api/', include('apps.payments.urls')),
    path('api/', include('apps.ledger.urls')),
    path('api/', include('apps.disputes.urls')),

]
