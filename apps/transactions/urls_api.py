from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet

router = DefaultRouter()
router.register(r'', TransactionViewSet)

urlpatterns = router.urls