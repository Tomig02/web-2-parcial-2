from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "email",
        "motivo",
        "fecha_creacion"
    )

    list_filter = ("motivo", "fecha_creacion")

    search_fields = ("nombre", "email", "mensaje")

    readonly_fields = ("fecha_creacion",)