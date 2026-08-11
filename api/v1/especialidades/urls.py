from rest_framework.routers import DefaultRouter

from .views import EspecialidadeViewSet


router = DefaultRouter()
router.register("", EspecialidadeViewSet, basename="especialidade")

urlpatterns = router.urls
