from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class ContactMessage(models.Model):

    CATEGORY_CHOICES = [
        ("comercial", "Consulta Comercial"),
        ("tecnica", "Consulta Técnica"),
        ("rrhh", "Consulta de RRHH"),
        ("general", "Consulta General"),
    ]

    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    motivo = models.CharField(max_length=20)
    mensaje = models.TextField()

    categoria = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="general"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def clasificar_mensaje(self):

        mensaje = self.mensaje.lower()

        if any(palabra in mensaje for palabra in [
            "precio", "costo", "tarifa", "compra"
        ]):
            return "comercial"

        elif any(palabra in mensaje for palabra in [
            "soporte", "error", "problema", "ayuda"
        ]):
            return "tecnica"

        elif any(palabra in mensaje for palabra in [
            "trabajo", "cv", "empleo", "linkedin"
        ]):
            return "rrhh"

        else:
            return "general"

    def save(self, *args, **kwargs):
        self.categoria = self.clasificar_mensaje()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.get_categoria_display()}"

class AllowedUser(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name="Correo electrónico"
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Usuario permitido"
        verbose_name_plural = "Usuarios permitidos"


class EmailVerification(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    code = models.CharField(max_length=6)

    token = models.UUIDField(default=uuid.uuid4, unique=True)

    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() <= self.expires_at


class Product(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    foto = models.CharField(
        max_length=255,
        default="sitio_web/producto/producto.jpg"
    )

    def __str__(self):
        return self.nombre