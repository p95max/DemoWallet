from rest_framework.routers import DefaultRouter
from .views import LedgerEntryViewSet

router = DefaultRouter()
router.register(r'', LedgerEntryViewSet)

urlpatterns = router.urls