from rest_framework import serializers
from .models import ContactMessage
from django.templatetags.static import static
from .models import Product
from decimal import Decimal, ROUND_HALF_UP


class ContactMessageSerializer(serializers.ModelSerializer):
    categoria = serializers.CharField(
        source="get_categoria_display",
        read_only=True
    )

    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "nombre",
            "email",
            "motivo",
            "mensaje",
            "categoria",
            "fecha_creacion",
        ]


class ProductSerializer(serializers.ModelSerializer):
    foto = serializers.SerializerMethodField()
    precio_usd = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "foto",
            "nombre",
            "descripcion",
            "precio",
            "precio_usd",
            "unidad",
            "categoria",
        ]

    def get_foto(self, obj):
        return static(obj.foto)

    def get_precio_usd(self, obj):
        dolar_venta = self.context.get("dolar_venta")

        if not dolar_venta:
            return None

        precio = obj.precio / dolar_venta

        return precio.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )