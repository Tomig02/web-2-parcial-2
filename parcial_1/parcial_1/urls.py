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
    path("panel/solicitudes/", views.ContactMessageListView.as_view(), name="panel_solicitudes"),
    path("panel/solicitudes/crear/", views.ContactMessageCreateView.as_view(), name="crear_solicitud" ),
    path("panel/solicitudes/editar/<int:pk>/", views.ContactMessageUpdateView.as_view(), name="editar_solicitud"),
    path("panel/solicitudes/eliminar/<int:pk>/", views.ContactMessageDeleteView.as_view(), name="eliminar_solicitud"),
    path("api/consultas/", views.ContactMessageAPIView.as_view(), name="api_solicitudes"),
]