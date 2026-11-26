import datetime
from datetime import timedelta
from decimal import Decimal, InvalidOperation
import secrets
from zoneinfo import ZoneInfo

import requests
from requests.exceptions import RequestException

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ContactForm, ContactMessageForm, LoginForm, RegisterForm, VerificationForm
from .models import AllowedUser, ContactMessage, EmailVerification, Product
from .serializers import ContactMessageSerializer, ProductSerializer

def landing(request):
    return render(request, 'sitio_web/landing.html')

# views.py
def blog(request):
    posts_mock = [
    {
        'title': '3 Semillas esenciales para activar tus mañanas',
        'featured_image': {'url': static('sitio_web/posts/semillas-mix.jpg')}, 
        'created_at': datetime.datetime.now(tz=ZoneInfo('America/Buenos_Aires')).date,
        'content': '<p>Sumá una cucharada de chía, lino o sésamo a tus yogures o smoothies.</p>',
        'tip_note': 'Dejalas en remojo 15 minutos en agua para mejorar su digestión.',
    },
    {
        'title': '¿Por qué elegir frascos de vidrio?',
        'featured_image': {'url': static('sitio_web/posts/frascos.jpg')},
        'created_at': datetime.datetime.now(tz=ZoneInfo('America/Buenos_Aires')).date,
        'content': '<p>Conservar tus alimentos en frascos herméticos de vidrio...</p>',
        'tip_note': 'Etiquetá la base del frasco con la fecha de compra.',
    }
]
    return render(request, 'sitio_web/blog.html', {'posts': posts_mock})


def productos(request):
    dolar_venta = None

    try:
        response = requests.get(
            "https://dolarapi.com/v1/dolares/oficial",
            timeout=5
        )
        response.raise_for_status()

        dolar_data = response.json()
        dolar_venta = Decimal(str(dolar_data["venta"]))

        if not dolar_venta.is_finite() or dolar_venta <= 0:
            dolar_venta = None

    except (
        RequestException,
        ValueError,
        KeyError,
        TypeError,
        InvalidOperation
    ):
        dolar_venta = None

    productos_db = Product.objects.all()

    serializer = ProductSerializer(
        productos_db,
        many=True,
        context={"dolar_venta": dolar_venta}
    )

    return render(request, "sitio_web/productos.html", {
        "productos": serializer.data,
        "dolar_venta": dolar_venta,
    })

def contacto(request):
    was_valid = False

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            ContactMessage.objects.create(
                nombre=form.cleaned_data["nombre"],
                email=form.cleaned_data["email_telefono"],
                motivo=form.cleaned_data["motivo"],
                mensaje=form.cleaned_data["mensaje"]
            )

            was_valid = True
            ##enviar_email(form.cleaned_data)
    
    form = ContactForm()
    return render(request, "sitio_web/contacto.html", {
        "form": form,
        "was_valid": was_valid
    })

def enviar_email(form_data):
    nombre = form_data.get('nombre')
    email_telefono = form_data.get('email_telefono')
    mensaje = form_data.get('mensaje')
    motivos_dict = {
        "productos": "Consulta sobre productos / stock",
        "pedido": "Consulta sobre un pedido",
        "mayorista": "Consulta mayorista",
        "otro": "Otro",
    }
    motivo_clave = form_data.get('motivo')
    motivo_texto = motivos_dict.get(motivo_clave, "No especificado")


    asunto_admin = f"[{motivo_texto}] Nueva consulta de {nombre}"    
    cuerpo_mensaje = (
        f"Has enviado un mensaje desde el formulario de contacto de la web:\n\n"
        f"Nombre completo: {nombre}\n"
        f"Motivo: {motivo_texto}\n\n"
        f"Mensaje:\n{mensaje}"
    )

    send_mail(
        subject=asunto_admin,
        message=cuerpo_mensaje,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email_telefono],
        fail_silently=False,
    )

def registro(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            # Verificar autorización
            if not AllowedUser.objects.filter(email=email).exists():
                messages.error(
                    request,
                    "Acceso restringido. No está autorizado a utilizar este sistema."
                )

                return redirect("registro")

            # Crear usuario inactivo
            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=form.cleaned_data["nombre"],
                last_name=form.cleaned_data["apellido"],
                password=form.cleaned_data["password"],
                is_active=False
            )

            # Generar código y token
            code = str(secrets.randbelow(900000) + 100000)

            verification = EmailVerification.objects.create(
                user=user,
                code=code,
                expires_at=timezone.now() + timedelta(minutes=15)
            )

            # Crear enlace
            link = request.build_absolute_uri(
                reverse(
                    "validar_cuenta",
                    args=[verification.token]
                )
            )

            # Enviar correo
            send_mail(
                subject="Validación de cuenta - Raíz Natural",
                message=f"""
                    Hola {user.first_name}:

                    Para validar tu cuenta ingresá al siguiente enlace:

                    {link}

                    Tu código de validación es: {code}

                    El código vence en 15 minutos.
                """,
                from_email=None,
                recipient_list=[email]
            )

            messages.success(
                request,
                "Le llegará un correo para validar su cuenta."
            )

            return redirect("registro")

    else:
        form = RegisterForm()

    return render(request, "sitio_web/formulario.html", {
        "form": form,
        "titulo": "Crear cuenta",
        "texto_boton": "Registrarme",
        "enlace_url": "login",
        "enlace_texto": "Ya tengo una cuenta",
    })


def validar_cuenta(request, token):

    verification = get_object_or_404(
        EmailVerification,
        token=token
    )

    form = None
    if request.method == "POST":
        code = request.POST.get("codigo", "").strip()

        if not verification.is_valid():
            messages.error(
                request,
                "El código de validación ha expirado."
            )

        elif code == verification.code:

            user = verification.user
            user.is_active = True

            user.save()

            verification.delete()

            messages.success(
                request,
                "Tu cuenta fue validada correctamente. Ya podés iniciar sesión."
            )

            return redirect("login")

        else:
            messages.error(
                request,
                "El código de validación es incorrecto."
            )
    else:
        form = VerificationForm()
    return render(request, "sitio_web/formulario.html", {
        "form": form,
        "titulo": "Validación de cuenta",
        "descripcion": "Ingresá el código que recibiste por correo electrónico.",
        "texto_boton": "Validar cuenta",
    })

def iniciar_sesion(request):

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("/")

    else:
        form = LoginForm()

    return render(request, "sitio_web/formulario.html", {
        "form": form,
        "titulo": "Iniciar sesión",
        "texto_boton": "Ingresar",
        "enlace_url": "registro",
        "enlace_texto": "Crear cuenta",
    })



@login_required
def cerrar_sesion(request):
    if request.method == "POST":
        logout(request)
    return redirect("/")

class AdminRequiredMixin(LoginRequiredMixin):
    login_url = "login"


from django.db.models import Count, Q


class ContactMessageListView(AdminRequiredMixin, ListView):

    model = ContactMessage
    template_name = "sitio_web/panel_solicitudes.html"
    context_object_name = "solicitudes"
    ordering = ["-fecha_creacion"]

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["estadisticas"] = ContactMessage.objects.aggregate(
            total=Count("id"),

            comercial=Count(
                "id",
                filter=Q(categoria="comercial")
            ),

            tecnica=Count(
                "id",
                filter=Q(categoria="tecnica")
            ),

            rrhh=Count(
                "id",
                filter=Q(categoria="rrhh")
            ),

            general=Count(
                "id",
                filter=Q(categoria="general")
            )
        )

        return context


class ContactMessageFormView(AdminRequiredMixin):
    model = ContactMessage
    form_class = ContactMessageForm
    template_name = "sitio_web/formulario.html"
    success_url = reverse_lazy("panel_solicitudes")
class ContactMessageCreateView(ContactMessageFormView, CreateView):
    extra_context = {
        "titulo": "Nueva solicitud",
        "texto_boton": "Crear solicitud",
    }
class ContactMessageUpdateView(ContactMessageFormView, UpdateView):
    extra_context = {
        "titulo": "Editar solicitud",
        "texto_boton": "Guardar cambios",
    }

class ContactMessageDeleteView(AdminRequiredMixin, DeleteView):
    model = ContactMessage
    template_name = "sitio_web/formulario.html"
    success_url = reverse_lazy("panel_solicitudes")

    extra_context = {
        "titulo": "Eliminar solicitud",
        "texto_boton": "Confirmar eliminación",
        "descripcion": "¿Estás seguro de que querés eliminar esta solicitud?",
        "es_eliminacion": True,
    }


class ContactMessageAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        solicitudes = ContactMessage.objects.all().order_by("-fecha_creacion")
        serializer = ContactMessageSerializer(solicitudes, many=True)

        return Response({
            "total": solicitudes.count(),
            "solicitudes": serializer.data
        }, status=status.HTTP_200_OK)