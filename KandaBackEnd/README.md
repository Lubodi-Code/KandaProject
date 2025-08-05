# Kanda Backend

Este proyecto implementa un sistema de autenticación de usuarios utilizando Django como framework web y MongoDB (a través de MongoEngine) como base de datos.

## Características

- Registro de usuarios con campos: username, email y password (hash seguro)
- Envío de correo de confirmación al registrarse
- Generación de token de confirmación único y seguro
- Activación de cuenta mediante enlace enviado por correo
- Manejo de errores: enlace expirado, token inválido, reenvío de correo
- Inicio de sesión solo para usuarios con cuenta activada

## Requisitos

- Python 3.8+
- Django 5.2+
- MongoEngine
- Six
- Cuenta de correo para enviar emails (Gmail u otro servicio SMTP)

## Configuración

1. Clona el repositorio

2. Crea y activa un entorno virtual:
   ```
   python -m venv venv
   venv\Scripts\activate  # En Windows
   source venv/bin/activate  # En macOS/Linux
   ```

3. Instala las dependencias:
   ```
   pip install django mongoengine python-dotenv six
   ```

4. Configura las variables de entorno en el archivo `.env`:
   ```
   DB_PASSWORD=tu_contraseña_mongodb
   SECRET_KEY=tu_clave_secreta
   EMAIL_HOST_USER=tu_correo@gmail.com
   EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion
   DEFAULT_FROM_EMAIL=KandaBackend <tu_correo@gmail.com>
   ```

   > **Nota**: Para Gmail, necesitarás generar una "contraseña de aplicación" en la configuración de seguridad de tu cuenta de Google.

5. Ejecuta las migraciones de Django:
   ```
   python manage.py migrate
   ```

6. Inicia el servidor de desarrollo:
   ```
   python manage.py runserver
   ```

## Flujo de Uso

1. **Registro**:
   - Accede a `http://localhost:8000/api/register/`
   - Completa el formulario con tu nombre de usuario, correo electrónico y contraseña
   - Recibirás un mensaje de confirmación indicando que se ha enviado un correo de activación

2. **Activación**:
   - Revisa tu correo electrónico y haz clic en el enlace de activación
   - Serás redirigido a una página confirmando que tu cuenta ha sido activada
   - Si el enlace ha expirado, puedes solicitar uno nuevo en `http://localhost:8000/api/resend-activation/`

3. **Inicio de Sesión**:
   - Accede a `http://localhost:8000/api/login/`
   - Ingresa tu nombre de usuario o correo electrónico y contraseña
   - Si la cuenta está activada, serás redirigido al dashboard

4. **Dashboard**:
   - Una vez autenticado, verás tu información de usuario en el dashboard
   - Puedes cerrar sesión haciendo clic en el botón correspondiente

## Estructura del Proyecto

- `api/models.py`: Define el modelo de usuario con MongoEngine
- `api/views.py`: Contiene las vistas para registro, activación, login, etc.
- `api/forms.py`: Formularios para registro y login
- `api/tokens.py`: Generador de tokens para activación de cuentas
- `api/auth_backends.py`: Backend de autenticación personalizado para MongoDB
- `api/templates/`: Plantillas HTML para las diferentes páginas

## Notas de Seguridad

- Las contraseñas se almacenan con hash seguro utilizando las funciones de Django
- Los tokens de activación expiran después de un tiempo configurable (por defecto, 2 días)
- Se implementan validaciones para evitar registros duplicados
- Se utilizan mensajes genéricos para evitar la enumeración de usuarios

## Configuración de CORS

El backend está configurado para permitir solicitudes CORS desde el frontend. La configuración se encuentra en `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'corsheaders',
    # ...
]

MIDDLEWARE = [
    # ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True
```

## Integración con el frontend

Este backend está diseñado para trabajar con el frontend de Vue.js ubicado en el directorio `KandaFrontEnd`. Asegúrate de que ambos estén en funcionamiento para probar la aplicación completa.