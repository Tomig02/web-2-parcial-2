from django.db import migrations


def cargar_datos(apps, schema_editor):
    Product = apps.get_model("sitio_web", "Product")
    AllowedUser = apps.get_model("sitio_web", "AllowedUser")

    productos = [
        ("Almendras Naturales", "Almendras naturales seleccionadas.", 4500, "500 g", "Frutos secos"),
        ("Nueces Mariposa", "Nueces mariposa seleccionadas.", 5200, "500 g", "Frutos secos"),
        ("Semillas de Chía", "Semillas de chía naturales.", 2800, "250 g", "Semillas"),
        ("Avena Tradicional", "Avena tradicional.", 1900, "500 g", "Cereales"),
        ("Lentejas", "Lentejas seleccionadas.", 2200, "500 g", "Legumbres"),
        ("Granola Natural", "Granola natural.", 3900, "400 g", "Cereales"),
        ("Semillas de Girasol", "Semillas de girasol.", 2400, "300 g", "Semillas"),
        ("Maní Tostado", "Maní tostado.", 2500, "500 g", "Frutos secos"),
    ]

    for nombre, descripcion, precio, unidad, categoria in productos:
        Product.objects.update_or_create(
            nombre=nombre,
            defaults={
                "descripcion": descripcion,
                "precio": precio,
                "unidad": unidad,
                "categoria": categoria,
            }
        )

    AllowedUser.objects.get_or_create(
        email="annavillegas@live.com.ar"
    )


def revertir_datos(apps, schema_editor):
    Product = apps.get_model("sitio_web", "Product")
    AllowedUser = apps.get_model("sitio_web", "AllowedUser")

    nombres = [
        "Almendras Naturales",
        "Nueces Mariposa",
        "Semillas de Chía",
        "Avena Tradicional",
        "Lentejas",
        "Granola Natural",
        "Semillas de Girasol",
        "Maní Tostado",
    ]

    Product.objects.filter(nombre__in=nombres).delete()
    AllowedUser.objects.filter(
        email="annavillegas@live.com.ar"
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("sitio_web", "0005_product"),
    ]

    operations = [
        migrations.RunPython(cargar_datos, revertir_datos),
    ]