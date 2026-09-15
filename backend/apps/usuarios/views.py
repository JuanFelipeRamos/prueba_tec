from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsuariosSerializers
from .models import Usuarios

class UsuariosViewSets(viewsets.ModelViewSet):
    queryset = Usuarios
    serializer_class = UsuariosSerializers
    permission_classes = [IsAuthenticated]

    # eliminar usuarios
    def destroy(self, request, *args, **kwargs):
        usuario_autenticado = self.request.user

        if usuario_autenticado.rol != "admin":
            return Response({
                "error": "debes ser administrador para eliminar a otros usuarios."
            })

        return Response({
            "message": "usuario borrado exitosamente."
        }, status=status.HTTP_200_OK)
