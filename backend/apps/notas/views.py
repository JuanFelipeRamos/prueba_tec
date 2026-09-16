#pylint: disable=no-member
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import NotasSerializers
from .models import Notas

class SoloAdministradores(permissions.BasePermission):
    def has_permission(self, request, view):
        # validar que el usuario no sea AnonymousUser y esté logueado
        if not request.user or not request.user.is_authenticated:
            return False

        # validar de forma estricta el rol de tu modelo
        return request.user.rol == "Administrador"

class NotasViewSets(viewsets.ModelViewSet):
    queryset = Notas.objects.all()
    serializer_class = NotasSerializers
    permission_classes = [SoloAdministradores]
