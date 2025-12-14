from django.contrib import admin
from .models import Usuarios, Ejercicios, UsuarioEjercicio

admin.site.register(Usuarios)
admin.site.register(Ejercicios)
admin.site.register(UsuarioEjercicio)