from rest_framework.routers import DefaultRouter

from .views import BloqueioAgendaViewSet, DisponibilidadeMedicoViewSet


router = DefaultRouter()
router.register("disponibilidades", DisponibilidadeMedicoViewSet, basename="agenda-disponibilidade")
router.register("bloqueios", BloqueioAgendaViewSet, basename="agenda-bloqueio")

urlpatterns = router.urls
