"""
URL configuration for parcial_1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sitio_web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name="landing"),
    path("contacto/", views.contacto, name="contacto"),
    path("blog/", views.blog, name="contacto"),
    path("productos/", views.productos, name="productos"),
    path("registro/", views.registro, name="registro"),
    path("validar/<uuid:token>/", views.validar_cuenta, name="validar_cuenta"),
    path("login/", views.iniciar_sesion, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path(
        "panel/solicitudes/",
        views.ContactMessageListView.as_view(),
        name="panel_solicitudes"
    ),
    path(
        "panel/solicitudes/crear/",
        views.ContactMessageCreateView.as_view(),
        name="crear_solicitud"
    ),
    path(
        "panel/solicitudes/editar/<int:pk>/",
        views.ContactMessageUpdateView.as_view(),
        name="editar_solicitud"
    ),
    path(
        "panel/solicitudes/eliminar/<int:pk>/",
        views.ContactMessageDeleteView.as_view(),
        name="eliminar_solicitud"
    ),
]