from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.conf import settings
from django.conf.urls.static import static

from config.settings import BASE_DIR

urlpatterns = [
    path('', include('apps.web.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # Web
    path('wallets/', include('apps.accounts.urls')),
    path('transactions/', include('apps.transactions.urls')),
    path('transfers/', include('apps.transfers.urls')),

    # APIs
    path('api/users/', include('apps.users.urls')),
    path('api/accounts/', include('apps.accounts.urls_api')),
    path('api/transactions/', include('apps.transactions.urls_api')),
    path('api/transfers/', include('apps.transfers.urls_api')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui-old'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root="/home/maxx/PycharmProjects/DemoWallet/static")