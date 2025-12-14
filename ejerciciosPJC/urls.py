from django.urls import path
from ejerciciosPJC import views

urlpatterns = [
    path('', views.index, name='index'),
    path('formulario/<str:tipo_form>/', views.index, name='mostrar_formulario'),
    path('iniciar_sesion/', views.index, name="iniciar_sesion"),
    path('registrar_usuario/', views.registrar_usuario, name="registrar_usuario"),
    path('confirmar_registro/<token>/', views.confirmar_registro, name="confirmar_registro"),
    path('confirmar_recuperacion_contrasena/', views.confirmar_recuperacion_contrasena, name="confirmar_recuperacion_contrasena"), 
    path('recuperar_contrasena/<str:uidb64>/<str:token>/', views.recuperar_contrasena, name="recuperar_contrasena"),
    path('cambiar_contrasena/', views.cambiar_contrasena, name="cambiar_contrasena"),
    path('cierra_sesion/', views.cerrar_sesion, name="cerrar_sesion"),
    path('ejercicio/<str:lenguaje>/<str:id_unico>/', views.ejercicio, name="ejercicio"),
    path('ejecuta_prueba/', views.ejecuta_prueba, name="ejecuta_prueba"),
    path('administrar_ejercicios/', views.administrar_ejercicios, name="administrar_ejercicios"),
    path('agregar_ejercicio/', views.agregar_ejercicio, name="agregar_ejercicio"),
    path('editar_ejercicio/<str:id_unico>/', views.editar_ejercicio, name="editar_ejercicio"),
    path('eliminar_ejercicio/<str:id_unico>/', views.eliminar_ejercicio, name="eliminar_ejercicio"),
    path('elimina_cuenta/', views.elimina_cuenta, name="elimina_cuenta")
]