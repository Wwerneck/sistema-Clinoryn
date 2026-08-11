from rest_framework.routers import DefaultRouter

from .views import ProntuarioViewSet


router = DefaultRouter()
router.register("", ProntuarioViewSet, basename="prontuario")

urlpatterns = router.urls
