#pylint: disable=no-member
from rest_framework import serializers
from .models import Notas

class NotasSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notas
        fields = ["id", "titulo", "texto", "estado", "posicion_x", "posicion_y"]

    def create(self, validated_data):
        titulo_mayus = validated_data.get("titulo").capitalize()
        texto_mayus = validated_data.get("texto").capitalize()

        validated_data["titulo"] = titulo_mayus
        validated_data["texto"] = texto_mayus

        return Notas.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.titulo = validated_data.get("titulo", instance.titulo).capitalize()
        instance.texto = validated_data.get("texto", instance.texto).capitalize()
        instance.estado = validated_data.get("estado", instance.estado)

        instance.posicion_x = validated_data.get("posicion_x", instance.posicion_x)
        instance.posicion_y = validated_data.get("posicion_y", instance.posicion_y)
        instance.save()
        return instance
