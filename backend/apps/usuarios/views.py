from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsuariosSerializers
from .models import Usuarios

class SoloAdministradores(permissions.BasePermission):
    def has_permission(self, request, view):
        # validar que el usuario no sea AnonymousUser y esté logueado
        if not request.user or not request.user.is_authenticated:
            return False

        # validar de forma estricta el rol de tu modelo
        return request.user.rol == "administrador"

class UsuariosViewSets(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializers
    permission_classes = [SoloAdministradores]

    # no permitir eliminar todos los usuarios administradores, debe haber al menos un administrador
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.rol == "administrador":
            admin_count = Usuarios.objects.filter(rol="administrador").count()
            if admin_count <= 1:
                return Response({
                    "error": "No se puede eliminar el último administrador."
                }, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)


    # no permitir desactivar todos los administradores, debe haber al menos un administrador activo
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.rol == "administrador" and instance.is_active and not request.data.get("is_active"):
            admin_count = Usuarios.objects.filter(rol="administrador", is_active=True).count()
            if admin_count <= 1:
                return Response({
                    "error": "No se puede desactivar o quitar el último administrador activo."
                }, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)


    @action( detail=False, methods=["get"], permission_classes=[IsAuthenticated], url_path="me")
    def me(self, request):
        serializer = UsuariosSerializers(request.user)
        return Response(serializer.data)
