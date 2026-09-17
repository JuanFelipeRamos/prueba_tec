from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotasViewSets, metricas_dashboard

router = DefaultRouter()
router.register(r"notas", NotasViewSets, basename = "nota")


urlpatterns = [
    path("metricas/", metricas_dashboard, name="metricas-dashboard"),
    path("", include(router.urls)),
]
