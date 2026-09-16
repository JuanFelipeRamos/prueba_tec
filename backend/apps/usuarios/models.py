from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuarios(AbstractUser):
    rol = models.CharField(max_length=14, choices=[
        ('usuario', 'Usuario'),
        ('administrador', 'Administrador'),
    ], default='usuario')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
