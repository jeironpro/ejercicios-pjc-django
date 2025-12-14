from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random, string

class Usuarios(BaseUserManager):
    """Manager para el modelo Usuarios"""
    def create_user(self, email, password=None, **extra_fields):
        """Crea un usuario con el correo electrónico y la contraseña proporcionadas"""
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico.")
        
        email = self.normalize_email(email)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Crea un superusuario con el correo electrónico y la contraseña proporcionadas"""
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    
class Usuarios(AbstractBaseUser, PermissionsMixin):
    """Modelo para el usuario"""
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = Usuarios()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        """Devuelve una representacion en string del usuario"""
        return f"{self.id_usuari}: {self.email}"
    
def genera_identificador():
    """Genera un identificador aleatorio de 6 caracteres"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class Ejercicios(models.Model):
    """Modelo para el ejercicio"""
    id_unico = models.CharField(max_length=6, unique=True, default=genera_identificador, editable=False)
    titulo = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50)
    tipo = models.CharField(max_length=30)
    enunciado = models.CharField(max_length=255)
    tareas = models.CharField(max_length=150)
    pistas = models.CharField(max_length=150)
    entrada = models.CharField(max_length=100)
    salida = models.CharField(max_length=100)
    definicion = models.CharField(max_length=70, null=True, blank=True)
    uml = models.CharField(max_length=80, null=True, blank=True)
    prueba = models.CharField(max_length=80)
    lenguaje = models.CharField(max_length=50)

    def __str__(self):
        """Devuelve una representacion en string del ejercicio"""
        return f"{self.id_unico})"
    
class UsuarioEjercicio(models.Model):
    """Modelo para el usuario ejercicio"""
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicios, on_delete=models.CASCADE)
    codigo_usuario = models.TextField(blank=True, null=True)

    class Meta:
        """Meta para el modelo UsuarioEjercicio"""
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'ejercicio'], name='unique_usuario_ejercicio')
        ]

    def __str__(self):
        """Devuelve una representacion en string del usuario ejercicio"""
        return f"{self.usuario.username}: {self.ejercicio}"