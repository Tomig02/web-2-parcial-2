from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm

class ContactForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre completo",
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Ej. Martina Rossi",
            "class": "form-input",
        })
    )

    email_telefono = forms.CharField(
        label="Email",
        max_length=150,
        widget=forms.EmailInput(attrs={
            "placeholder": "tuemail@ejemplo.com",
            "class": "form-input",
        })
    )

    motivo = forms.ChoiceField(
        label="Motivo de consulta",
        choices=[
            ("productos", "Consulta sobre productos / stock"),
            ("pedido", "Consulta sobre un pedido"),
            ("mayorista", "Consulta mayorista"),
            ("otro", "Otro"),
        ],
        widget=forms.Select(attrs={
            "class": "form-input",
        })
    )

    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={
            "placeholder": "Escribí tu mensaje acá...",
            "class": "form-input form-textarea",
            "rows": 5,
        })
    )

from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):

    class Meta:
        model = ContactMessage

        fields = [
            "nombre",
            "email",
            "motivo",
            "mensaje"
        ]

        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-input"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-input"
            }),
            "motivo": forms.TextInput(attrs={
                "class": "form-input"
            }),
            "mensaje": forms.Textarea(attrs={
                "class": "form-input",
                "rows": 5
            })
        }

class RegisterForm(forms.Form):

    nombre = forms.CharField(
        label="Nombre",
        max_length=150
    )

    apellido = forms.CharField(
        label="Apellido",
        max_length=150
    )

    email = forms.EmailField(
        label="Correo electrónico"
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()

        if User.objects.filter(username=email).exists():
            raise forms.ValidationError(
                "Este correo ya tiene una cuenta registrada."
            )

        return email

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "placeholder": "tuemail@ejemplo.com"
        })
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )

    error_messages = {
        "invalid_login": (
            "Correo electrónico o contraseña incorrectos."
        ),
        "inactive": "Esta cuenta todavía no fue validada."
    }