from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotasViewSets

router = DefaultRouter()
router.register(r"notas", NotasViewSets, basename = "nota")


urlpatterns = [
    path("", include(router.urls)),
]