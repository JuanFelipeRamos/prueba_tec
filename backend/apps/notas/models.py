from django.db import models

class Notas(models.Model):
    titulo = models.CharField(max_length=100)
    texto = models.TextField()
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('en curso', 'En curso'),
        ('hecho', 'Hecho')
    ], default='pendiente')
    posicion_x = models.IntegerField()
    posicion_y = models.IntegerField()

    def __str__(self):
        return f"{self.titulo}"
