import logging
import tempfile
import subprocess
import json
import re
import os
import glob
import shutil
from .models import Usuarios, Ejercicios, UsuarioEjercicio
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import genera_token, verifica_token
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pathlib import Path

# Log
logger = logging.getLogger(__name__)

# Constantes
LENGUAJES_SOPORTADOS = {"Python", "Java", "Cpp"}

# Controladores
def index(request, tipo_form='iniciar_sesion'):
    """Controlador para la pagina principal que maneja el inicio de sesión y el registro de usuarios"""
    ejercicios = Ejercicios.objects.all()

    if request.method == "POST":
        correo_electronico = request.POST.get('email')
        contrasena = request.POST.get('password')
        usuario = authenticate(username=correo_electronico, password=contrasena)

        if usuario:
            login(request, usuario)
        else:
            messages.error(request, "Usuario o contraseña incorrecto")
        return redirect('index')

    if tipo_form not in ['registro', 'recupera_contrasena', 'iniciar_sesion']:
        tipo_form = 'iniciar_sesion'

    return render(request, 'ejerciciosPJC/index.html', {
        'ejercicios': ejercicios,
        'formulario': tipo_form,
    })

def registrar_usuario(request):
    """Controlador para el registro de usuarios"""
    if request.method == "POST":
        correo_electronico = request.POST['email']
        contrasena = request.POST['password']

        if Usuarios.objects.filter(email=correo_electronico).exists():
            messages.error(request, "El correo electrónico ya está registrado")
        else:
            enviar_confirmacion(request, correo_electronico, contrasena)
            messages.success(request, "Te hemos enviado un correo para confirmar tu cuenta.")
        return redirect('index')
    return redirect('index')

def enviar_confirmacion(request, correo_electronico, contrasena):
    """Controlador para enviar la confirmacion de registro"""
    current_site = get_current_site(request)
    asunto = "Bienvenido/a a Ejercicios PJC"

    datos = {
        'correo_electronico': correo_electronico,
        'contrasena': make_password(contrasena),
    }

    token = signing.dumps(datos)

    cuerpo = render_to_string('ejerciciosPJC/emails/confirma_registro.html', {
        'domain': current_site.domain,
        'token': token,
    })
    email_obj = EmailMessage(
        asunto,
        cuerpo,
        settings.EMAIL_HOST_USER,
        [correo_electronico]
    )
    email_obj.content_subtype = "html"
    email_obj.fail_silently = True
    email_obj.send()

def confirmar_registro(request, token):
    """Controlador para confirmar el registro de usuarios"""
    try:
        datos = signing.loads(token, max_age=3600)
        correo_electronico = datos['correo_electronico']
        contrasena = datos['contrasena']

        if Usuarios.objects.filter(email=correo_electronico).exists():
            messages.success(request, "Este correo ya ha sido registrado.")
        else:
            usuario = Usuarios(username=correo_electronico, email=correo_electronico, password=contrasena)
            usuario.is_active = True
            usuario.save()
            login(request, usuario)
            messages.success(request, "Su cuenta esta activada")
    except (signing.BadSignature, KeyError, TypeError):
        messages.error(request, "El enlace no es válido o ha expirado.")
    return redirect('index')

def confirmar_recuperacion_contrasena(request):
    """Controlador para confirmar la recuperacion de contrasena"""
    if request.method == "POST":
        email = request.POST.get("email")
        usuario = Usuarios.objects.filter(email=email).first()

        if usuario:
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(usuario.pk))
            token_gen = genera_token(usuario)

            cuerpo = render_to_string('ejerciciosPJC/emails/confirma_recupera_contrasena.html', {
                'domain': current_site.domain,
                'uid': uid,
                'token': token_gen,
            })

            email_obj = EmailMessage(
                "Recuperación de contraseña",
                cuerpo,
                settings.EMAIL_HOST_USER,
                [usuario.email]
            )
            email_obj.content_subtype = "html"
            email_obj.fail_silently = True
            email_obj.send()

        messages.success(request, "Si estás registrado, recibirás un correo de recuperación.")
        return redirect('index')

    ejercicios = Ejercicios.objects.all()
    return render(request, 'ejerciciosPJC/index.html', {
        'ejercicios': ejercicios,
        'formulario': 'recupera_contrasena'
    })

def recuperar_contrasena(request, uidb64, token):
    """Controlador para recuperar la contrasena"""
    ejercicios = Ejercicios.objects.all()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = Usuarios.objects.get(pk=uid)

        if usuario and verifica_token(token):
            return render(request, 'ejerciciosPJC/index.html', {
                'ejercicios': ejercicios,
                'formulario_contrasena': True,
                'uidb64': uidb64,
                'token': token,
            })
    except (TypeError, ValueError, OverflowError, Usuarios.DoesNotExist):
        pass

    messages.error(request, "El enlace no es válido o ha expirado.")
    return redirect('index')

def cambiar_contrasena(request):
    """Controlador para cambiar la contrasena"""
    if request.method != "POST":
        return redirect('index')

    uidb64 = request.POST.get("uidb64")
    token = request.POST.get("token")
    contrasena = request.POST.get("contrasena")

    if not uidb64 or not token:
        messages.error(request, "Faltan datos necesarios.")
        return redirect('index')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = Usuarios.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuarios.DoesNotExist):
        usuario = None

    if not usuario or not verifica_token(token):
        messages.error(request, "El enlace no es válido o ha expirado.")
        return redirect('index')

    if usuario.check_password(contrasena):
        messages.error(request, "Tu nueva contraseña no puede ser igual a la anterior.")
        return redirect('index')

    usuario.set_password(contrasena)
    usuario.save()
    login(request, usuario)

    messages.success(request, "Contraseña cambiada correctamente.")
    return redirect('index')

@login_required()
def cerrar_sesion(request):
    """Controlador para cerrar la sesion"""
    logout(request)
    return redirect('index')

def ejercicio(request, id_unico, lenguaje):
    """Controlador para el ejercicio"""
    ejercicio = get_object_or_404(Ejercicios, id_unico=id_unico, lenguaje=lenguaje)
    codigo_ejercicio = ejercicio.definicion

    if request.user.is_authenticated:
        usuario_ejercicio = UsuarioEjercicio.objects.filter(usuario=request.user, ejercicio=ejercicio).first()

        if usuario_ejercicio:
            codigo_ejercicio = usuario_ejercicio.codigo_usuario

    return render(request, 'ejerciciosPJC/ejercicio.html', {'ejercicio': ejercicio, 'codigo_ejercicio': codigo_ejercicio})

@csrf_exempt
def ejecuta_prueba(request):
    """Controlador para ejecutar la prueba"""
    if request.method == "POST":

        try:
            datos = json.loads(request.body)
            codigo_usuario = datos.get("codigo")
            id_unico = datos.get("id_unico")
            lenguaje = datos.get("lenguaje")
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
        
        if not codigo_usuario or not id_unico or not lenguaje:
            return JsonResponse({"error": "Faltán parámetros obligatorios"}, status=400)
        
        if lenguaje not in LENGUAJES_SOPORTADOS:
            return JsonResponse({"error": "Lenguaje {lenguaje} no soportado"}, status=400)
        

        ejercicio = get_object_or_404(Ejercicios, id_unico=id_unico)
        usuario = request.user if request.user.is_authenticated else None

        if not usuario:
            return JsonResponse({"error": "Usuario no autenticado"}, status=401)

        usuario_ejercicio, created = UsuarioEjercicio.objects.get_or_create(
            usuario=usuario, 
            ejercicio=ejercicio, 
            defaults={"codigo_usuario": codigo_usuario}
        )

        if not created:
            usuario_ejercicio.codigo_usuario = codigo_usuario
            usuario_ejercicio.save(update_fields=['codigo_usuario'])

        try:
            if lenguaje == "Python":
                resultado = ejecuta_python(codigo_usuario)
                print(resultado)
                os.remove("pruebas/python/codigo_usuario.py")
            elif lenguaje == "Java":
                resultado = ejecuta_java(ejercicio, codigo_usuario)
                os.remove(f"pruebas/java/{ejercicio.titulo}.java")
            elif lenguaje == "C++":
                resultado = ejecuta_cpp(ejercicio, codigo_usuario)
                os.remove(f"pruebas/cpp/{ejercicio.titulo}.cpp")
        except Exception as e:
            logger.exception("Error ejecutando código")
            return JsonResponse({"error": "Error interno al ejecutar el código", "detalles": str(e)}, status=500)

        if resultado is None:
            return JsonResponse({"error": "No se pudo ejecutar el código"}, status=500)
        
        if resultado.returncode != 0:
            return JsonResponse({
                "error": "Error en la ejecución o compilación",
                "detalles": resultado.stderr.strip()
            }, status=400)
        
        resultados = []
        for linea in resultado.stdout.strip().splitlines():
            try:
                nombre_prueba, esperado, obtenido = linea.split(":", 2)
                resultados.append({
                    "prueba": nombre_prueba,
                    "esperado": esperado,
                    "resultado": obtenido
                })
            except ValueError:
                logger.warning(f"Línea de salida inválida: {linea}")
                continue
        
        # Limpieza
        limpia_dir_python()
        limpia_dir_java()
        limpia_dir_cpp()

        return JsonResponse({"resultados": resultados})

def ejecuta_python(codigo_usuario):
    """Funcion para ejecutar el codigo python"""
    with tempfile.TemporaryDirectory(prefix="prueba_python_") as tmpdir:
        codigo_path = Path(tmpdir) / "codigo_usuario.py"
        with open(codigo_path, "w", encoding="utf-8") as f:
            f.write(codigo_usuario)

        match = re.search(r'def\s+(\w+)\s*(', codigo_usuario)

        if not match:
            raise ValueError("No se encontró función definida en el código Python")
        
        nombre_func = match.group(1)
        sel_test = f"test_{nombre_func}.py"

        resultado = subprocess.run(
            ["python3", "-m", "unittest", sel_test], 
            cwd=tmpdir, 
            capture_output=True, 
            text=True,
            timeout=10
        )
        return resultado

def ejecuta_java(ejercicio, codigo_usuario):
    """Funcion para ejecutar el codigo java"""
    with tempfile.TemporaryDirectory(prefix="prueba_java_") as tmpdir:
        nombre = ejercicio.definicion
        java_file = Path(tmpdir) / f"{nombre}.java"

        with open(java_file, "w", encoding="utf-8") as f:
            f.write(codigo_usuario)

        with open(java_file, "r", encoding="utf-8") as f:
            contenido = f.read()
        
        match = re.search(r'public\s+class\s+(\w+)', contenido)
        if not match:
            raise ValueError("No se encontró clase pública en el código Java")
        
        nombre_clase = match.group(1)
        sel_test = f"{nombre_clase}Test.java"

        compilacion = subprocess.run(
            ["javac", "-d", tmpdir, str(java_file), str(Path(tmpdir) / sel_test)],
            capture_output=True, 
            text=True,
            timeout=15
        )

        if compilacion.returncode != 0:
            raise RuntimeError(f"Error compilando Java: {compilacion.stderr.strip()}")
        
        ejecucion = subprocess.run(
            ["java", "-cp", tmpdir, f"{nombre_clase}Test"],
            capture_output=True,
            text=True,
            timeout=10    
        )
        return ejecucion

def ejecuta_cpp(ejercicio, codigo_usuario):
    """Funcion para ejecutar el codigo cpp"""
    with tempfile.TemporaryDirectory(prefix="prueba_cpp_") as tmpdir:
        nombre = ejercicio.definicion
        cpp_file = Path(tmpdir) / f"{nombre}.cpp"
        test_file = Path(tmpdir) / f"{nombre}Test.cpp"
        ejecutable = Path(tmpdir) / f"{nombre}TestExec"

        with open(cpp_file, "w", encoding="utf-8") as f:
            f.write(codigo_usuario)

        compilacion = subprocess.run(
            ["g++", str(cpp_file), str(test_file), "-o", str(ejecutable)],
            capture_output=True, 
            text=True,
            timeout=20
        )

        if compilacion.returncode != 0:
            raise RuntimeError(f"Error compilando c++: {compilacion.stderr.strip()}")
        
        ejecucion = subprocess.run(
            [str(ejecutable)],
            capture_output=True,
            text=True,
            timeout=10    
        )
        return ejecucion

def limpia_dir_python():
    """Funcion para limpiar el directorio de pruebas python"""
    ruta_cache = Path("pruebas/python/__pycache__")
    if ruta_cache.exists():
        shutil.rmtree(ruta_cache)
        
def limpia_dir_java():
    """Funcion para limpiar el directorio de pruebas java"""
    for class_file in glob.glob("pruebas/java/*.class"):
        try:
            os.remove(class_file)
        except OSError:
            logger.warning(f"No se pudo eliminar {class_file}")

def limpia_dir_cpp():
    """Funcion para limpiar el directorio de pruebas cpp"""
    ruta_cpp = Path("pruebas/cpp/")
    for archivo in ruta_cpp.iterdir():
        if archivo.is_file() and archivo.suffix == "":
            try:
                archivo.unlink()
            except OSError:
                logger.warning(f"No se pudo eliminar {archivo}")

@login_required()
def elimina_cuenta(request):
    """Controlador para eliminar la cuenta"""
    if request.method == "POST" or "GET":
        if request.user.is_authenticated:
            request.user.delete()
    return redirect('index')

# Administración
def verifica_login_superusuario(vista):
    """Funcion para verificar el login y superusuario"""
    @login_required
    def verifica_superusuario(request, *args, **kwargs):
        if not request.user.is_superuser:
            return None
        return vista(request, *args, **kwargs)

    return verifica_superusuario

@verifica_login_superusuario
def administrar_ejercicios(request):
    """Controlador para administrar los ejercicios"""
    ejercicios = Ejercicios.objects.all()

    return render(request, 'ejerciciosPJC/administrar_ejercicios.html', {'ejercicios': ejercicios})

@verifica_login_superusuario
def agregar_ejercicio(request):
    """Controlador para agregar ejercicios"""
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        nivel = request.POST.get('nivel')
        tipo = request.POST.get('tipo')
        enunciado = request.POST.get('enunciado')
        tareas = request.POST.get('tareas')
        pistas = request.POST.get('pistas')
        entrada = request.POST.get('entrada')
        salida = request.POST.get('salida')
        definicion = request.POST.get('definicion')
        uml = request.POST.get('uml')
        prueba = request.POST.get('prueba')
        lenguaje = request.POST.get('lenguaje')

        ejercicio = Ejercicios(
            titulo = titulo,
            nivel = nivel,
            tipo = tipo,
            enunciado = enunciado,
            tareas = tareas,
            pistas = pistas,
            entrada = entrada,
            salida = salida,
            definicion = definicion,
            uml = uml,
            prueba = prueba,
            lenguaje = lenguaje
        )
        ejercicio.save()
    return redirect('administrar_ejercicios')

@verifica_login_superusuario
def editar_ejercicio(request, id_unico):
    """Controlador para editar ejercicios"""
    ejercicio = Ejercicios.objects.get(id_unico=id_unico)

    if request.method == "POST":
        titulo = request.POST.get('titulo')
        nivel = request.POST.get('nivel')
        tipo = request.POST.get('tipo')
        enunciado = request.POST.get('enunciado')
        tareas = request.POST.get('tareas')
        pistas = request.POST.get('pistas')
        entrada = request.POST.get('entrada')
        salida = request.POST.get('salida')
        definicion = request.POST.get('definicion')
        uml = request.POST.get('uml')
        prueba = request.POST.get('prueba')
        lenguaje = request.POST.get('lenguaje')

        ejercicio.titulo = titulo
        ejercicio.nivel = nivel
        ejercicio.tipo = tipo
        ejercicio.enunciado = enunciado
        ejercicio.tareas = tareas
        ejercicio.pistas = pistas
        ejercicio.entrada = entrada
        ejercicio.salida = salida
        ejercicio.definicion = definicion
        ejercicio.uml = uml
        ejercicio.prueba = prueba
        ejercicio.lenguaje = lenguaje

        ejercicio.save(update_fields=[
            'titulo',
            'nivel',
            'tipo',
            'enunciado',
            'tareas',
            'pistas',
            'entrada',
            'salida',
            'definicion',
            'uml',
            'prueba',
            'lenguaje'
        ])
    return redirect('administrar_ejercicios')

@verifica_login_superusuario
def eliminar_ejercicio(request, id_unico):
    """Controlador para eliminar ejercicios"""
    ejercicio = Ejercicios.objects.filter(id_unico=id_unico)

    if request.method == "POST" or "GET":
        ejercicio.delete()
    return redirect('administrar_ejercicios')