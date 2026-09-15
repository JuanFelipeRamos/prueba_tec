from rest_framework import serializers
from .models import Usuarios

class UsuariosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ["id", "username", "email", "password", "rol", "is_active"]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    # validar que el usuario autenticado sea admin
    def validate(self, data):
        usuario_autenticado = self.context['request'].user

        if usuario_autenticado.rol != "admin":
            raise serializers.ValidationError(
                "debes ser administrador para realizar esta acción."
            )
        return data

    # crear usuarios
    def create(self, validated_data):
        pwd = validated_data.pop("password")
        user = Usuarios(**validated_data)

        user.set_password(pwd)
        user.save()

        return user
