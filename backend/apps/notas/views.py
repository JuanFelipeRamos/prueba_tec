#pylint: disable=no-member
import json
from django.http import JsonResponse
from rest_framework import viewsets
from lambda_metricas.handler import lambda_handler
from .serializers import NotasSerializers
from .models import Notas

class NotasViewSets(viewsets.ModelViewSet):
    queryset = Notas.objects.all()
    serializer_class = NotasSerializers


def metricas_dashboard(request):
    resultado = lambda_handler({}, None)
    datos = json.loads(resultado["body"])
    return JsonResponse(datos, status=resultado["statusCode"])
