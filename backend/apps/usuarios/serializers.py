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

    # crear usuarios
    def create(self, validated_data):
        pwd = validated_data.pop("password")
        user = Usuarios(**validated_data)

        user.set_password(pwd)
        user.save()

        return user
