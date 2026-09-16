from django.contrib import admin
from .models import Notas

@admin.register(Notas)
class NotasAdmin(admin.ModelAdmin):
    list_display = ("titulo", "estado")
