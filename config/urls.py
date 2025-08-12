from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def redirect_to_swagger(request):
    return redirect('swagger-ui')

urlpatterns = [
    path('', redirect_to_swagger),
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/transactions/', include('apps.transactions.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/ledger/', include('apps.ledger.urls')),
    path('api/disputes/', include('apps.disputes.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui-old'),
]