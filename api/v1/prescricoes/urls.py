from rest_framework.routers import DefaultRouter

from .views import PrescricaoViewSet


router = DefaultRouter()
router.register("", PrescricaoViewSet, basename="prescricao")

urlpatterns = router.urls
