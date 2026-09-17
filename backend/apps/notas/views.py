#pylint: disable=no-member
from rest_framework import viewsets
from .serializers import NotasSerializers
from .models import Notas

class NotasViewSets(viewsets.ModelViewSet):
    queryset = Notas.objects.all()
    serializer_class = NotasSerializers
