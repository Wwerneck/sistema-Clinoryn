from rest_framework.routers import DefaultRouter

from .views import MedicoViewSet


router = DefaultRouter()
router.register("", MedicoViewSet, basename="medico")

urlpatterns = router.urls
