# ejercicios-pjc-django

## 📌 Descripción
Este proyecto forma parte de mi portafolio personal.  
El objetivo es demostrar buenas prácticas de programación, organización y documentación en GitHub.

## 🚀 Instalación

Sigue estos pasos para configurar y ejecutar el proyecto localmente:

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/jeironpro/ejercicios-pjc-django.git
    cd ejercicios-pjc-django
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv

    # Activa el entorno virtual:
    - En Windows
    .\venv\Scripts\activate
    
    - En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura las variables de entorno:**
    Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables (ejemplo):
    ```
    Actualmente se usa DJANGO_SECRET_KEY con la clave generada por django-admin startproject. 
    - Para cambiarla agrega la siguiente variable de entorno:
    SECRET_KEY='tu_clave_secreta_de_django' # Genera una clave segura

    - Y en el archivo settings.py:
    · Importa os al inicio del archivo:
    import os
    
    · Agrega la siguiente línea:
    DJANGO_SECRET_KEY = os.getenv('SECRET_KEY')
   
    - Si cambia la base de datos, agrega las siguientes variables de entorno:
    USER_DB='tu_usuario_de_base_de_datos'
    PASSWORD_DB='tu_contraseña_de_base_de_datos'
    HOST_DB='tu_host_de_base_de_datos'
    PORT_DB='tu_puerto_de_base_de_datos'
    
    Y en el archivo settings.py:
    · Importa os al inicio del archivo:
    import os
    
    · Editar:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.tipo_de_base_de_datos',
            'NAME': BASE_DIR / 'nombre_de_la_base_de_datos',
            'USER': os.getenv('USER_DB'),
            'PASSWORD': os.getenv('PASSWORD_DB'),
            'HOST': os.getenv('HOST_DB'),
            'PORT': os.getenv('PORT_DB'),
        }
    }

    - Variables de configuración de envio de correos electrónicos:
    EMAIL_HOST_USER = 'tu_correo@gmail.com'
    EMAIL_HOST_PASSWORD = 'tu_contraseña_de_gmail'

    - Y en el archivo settings.py:
    · Importa os al inicio del archivo:
    import os
    
    · Agrega la siguiente línea:
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    ```

5.  **Aplica las migraciones de la base de datos:**
    ```bash
    python manage.py migrate
    ```

6.  **Crea un superusuario (opcional):**
    ```bash
    python manage.py createsuperuser
    ```

## 🛠️ Uso

Para iniciar el servidor de desarrollo de Django:

```bash
python manage.py runserver
```

Una vez que el servidor esté en funcionamiento, puedes acceder a la aplicación en tu navegador web en `http://127.0.0.1:8000/`.


## 🧪 Administración de Ejercicios y Pruebas

### Gestión de Ejercicios desde el Panel de Administración

Para añadir nuevos ejercicios o modificar los existentes, sigue estos pasos:

1.  Asegúrate de que el servidor de desarrollo esté en ejecución (`python manage.py runserver`).
2.  Accede al panel de administración de Django en `http://127.0.0.1:8000/admin/`.
3.  Inicia sesión con las credenciales de un superusuario.
4.  Dentro del panel, busca la sección correspondiente al modelo "Ejercicios".
5.  Haz clic en "Añadir" para crear un nuevo ejercicio o en el nombre de un ejercicio existente para editarlo.
6.  Rellena los campos necesarios, como el título, la descripción, el nivel de dificultad, etc.

### Agregando Archivos de Prueba

Los archivos de prueba son esenciales para la evaluación automática de los ejercicios. Deben organizarse en la carpeta `pruebas` dentro de la estructura del proyecto, siguiendo una convención específica para cada ejercicio.

**Estructura de la carpeta `pruebas`:**
    Dentro de la carpeta `pruebas`, hay subcarpetas para cada lenguaje de programación, dentro de cada subcarpeta se deben crear las pruebas con la siguiente nomenclatura:
    - para python: test_nombre_funcion.py. (nombre_funcion es el nombre de la definición que se ha creado en el ejercicio).
    - para java: NombreClaseTest.java. (NombreClase es el nombre de la clase que se ha creado en el ejercicio).
    - para cpp: DefinicionTest.cpp. (Definicion es el nombre de la definición que se ha creado en el ejercicio).
    
    ```
    pruebas/
    ├── python/
    │   ├── test_nombre_funcion.py
    │   └── ...
    ├── java/
    │   ├── NombreClaseTest.java
    │   └── ...
    ├── cpp/
    │   ├── DefinicionTest.cpp
    │   └── ...
    └── ...
    ```
```

## ✨ Características

*   **Gestión de Usuarios:** Autenticación y autorización básica.
*   **Vistas y URLs:** Implementación de vistas basadas en funciones y clases.
*   **Plantillas:** Uso del sistema de plantillas de Django para renderizar HTML.
*   **Admin Panel:** Configuración del panel de administración de Django.

## 🛠️ Tecnologías Utilizadas

*   **Python:** Lenguaje de programación principal.
*   **Django:** Framework web para el desarrollo rápido.
*   **SQLite:** Base de datos por defecto (puede ser configurada para PostgreSQL, MySQL, etc.).
*   **HTML/CSS:** Para la interfaz de usuario.
*   **Git:** Control de versiones.
```

## 📝 Nota
Este proyecto fue creado hace aproximadamente 8 meses, por lo que puede que no sea el mejor ejemplo de un proyecto de Django, lo he abandonado por estar aprendiendo otras tecnologías y he decidido hacerlo publico ya que no pienso continuarlo.

## 📜 Licencia
Este proyecto está bajo la licencia **MIT**.  
Consulta el archivo [LICENSE](LICENSE) para más detalles.
