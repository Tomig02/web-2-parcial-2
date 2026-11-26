import secrets
import datetime
from zoneinfo import ZoneInfo

from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.templatetags.static import static

from .models import ContactMessage, AllowedUser, EmailVerification
from .forms import ContactForm, RegisterForm, LoginForm

from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import (ListView, CreateView, UpdateView, DeleteView)

from django.urls import reverse_lazy

from .models import ContactMessage
from .forms import ContactMessageForm

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
    from django.shortcuts import render


def productos(request):
    productos = [
        {
            "foto": static('sitio_web/producto/producto.jpg'),
            "nombre": "Almendras Naturales",
            "descripcion": "Almendras seleccionadas, sin sal ni agregados.",
            "precio": 4500,
            "unidad": "500 g",
            "categoria": "Frutos secos",
        },
        {
            "foto": static('sitio_web/producto/producto.jpg'),
            "nombre": "Nueces Mariposa",
            "descripcion": "Nueces de excelente calidad, ideales para tus comidas.",
            "precio": 5200,
            "unidad": "500 g",
            "categoria": "Frutos secos",
        },
        {
            "foto": static('sitio_web/producto/producto.jpg'),
            "nombre": "Semillas de Chía",
            "descripcion": "Fuente natural de fibra y nutrientes.",
            "precio": 2800,
            "unidad": "250 g",
            "categoria": "Semillas",
        },
        {
            "foto": static('sitio_web/producto/producto.jpg'),
            "nombre": "Avena Tradicional",
            "descripcion": "Avena en hojuelas para desayunos y preparaciones.",
            "precio": 1900,
            "unidad": "500 g",
            "categoria": "Cereales",
        },
        {
            "foto": static('sitio_web/producto/producto.jpg'),
            "nombre": "Lentejas",
            "descripcion": "Legumbres seleccionadas, nutritivas y versátiles.",
            "precio": 2200,
            "unidad": "500 g",
            "categoria": "Legumbres",
        },
        {
            "foto": static('sitio_web/producto/producto.jpg'),
            "nombre": "Granola Natural",
            "descripcion": "Mezcla crocante de avena, frutos secos y semillas.",
            "precio": 3900,
            "unidad": "400 g",
            "categoria": "Cereales",
        },
        {
            "foto": static('sitio_web/producto/producto.jpg'),
            "nombre": "Semillas de Girasol",
            "descripcion": "Semillas naturales, ideales para ensaladas y snacks.",
            "precio": 2400,
            "unidad": "300 g",
            "categoria": "Semillas",
        },
        {
            "foto": static('sitio_web/producto/producto.jpg'),
            "nombre": "Maní Tostado",
            "descripcion": "Maní tostado sin sal, simple y delicioso.",
            "precio": 2500,
            "unidad": "500 g",
            "categoria": "Frutos secos",
        },
    ]

    return render(request, "sitio_web/productos.html", {
        "productos": productos,
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

    return render(request, "sitio_web/registro.html", {
        "form": form
    })


def validar_cuenta(request, token):

    verification = get_object_or_404(
        EmailVerification,
        token=token
    )

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

    return render(request, "sitio_web/validar_cuenta.html")

def iniciar_sesion(request):

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("/")

    else:
        form = LoginForm()

    return render(request, "sitio_web/login.html", {
        "form": form
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


class ContactMessageCreateView(AdminRequiredMixin, CreateView):

    model = ContactMessage
    form_class = ContactMessageForm

    template_name = "sitio_web/solicitud_form.html"
    success_url = reverse_lazy("panel_solicitudes")

class ContactMessageUpdateView(AdminRequiredMixin, UpdateView):

    model = ContactMessage
    form_class = ContactMessageForm

    template_name = "sitio_web/solicitud_form.html"
    success_url = reverse_lazy("panel_solicitudes")

class ContactMessageDeleteView(AdminRequiredMixin, DeleteView):

    model = ContactMessage

    template_name = "sitio_web/solicitud_confirm_delete.html"
    success_url = reverse_lazy("panel_solicitudes")