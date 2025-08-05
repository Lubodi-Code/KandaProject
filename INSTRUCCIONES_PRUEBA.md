# Instrucciones para probar el flujo de registro, activación y login

Este documento proporciona instrucciones detalladas para probar el flujo completo de registro, activación de cuenta y login en la aplicación KandaProyect.

## Requisitos previos

1. Tener instalado Python 3.8+ y Node.js 14+
2. Tener MongoDB instalado y en ejecución
3. Tener todas las dependencias instaladas en el backend y frontend

## Configuración del entorno

### Backend (Django)

1. Navega a la carpeta del backend:
   ```
   cd KandaBackEnd
   ```

2. Verifica que el archivo `.env` contenga las credenciales correctas para el correo electrónico:
   ```
   EMAIL_HOST_USER=tu_correo@gmail.com
   EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicación
   DEFAULT_FROM_EMAIL=tu_correo@gmail.com
   ```

   > **Nota**: Si usas Gmail, debes generar una "contraseña de aplicación" en la configuración de seguridad de tu cuenta de Google.

3. Para pruebas locales, puedes configurar Django para que muestre los correos en la consola en lugar de enviarlos realmente. Modifica `settings.py` temporalmente:
   ```python
   # Comentar la configuración actual de EMAIL_BACKEND
   # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   # Y añadir esta línea para mostrar los correos en la consola
   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   ```

4. Inicia el servidor de Django:
   ```
   python manage.py runserver
   ```

### Frontend (Vue.js)

1. Navega a la carpeta del frontend:
   ```
   cd KandaFrontEnd
   ```

2. Inicia el servidor de desarrollo:
   ```
   npm run dev
   ```

## Prueba del flujo completo

### 1. Registro de usuario

1. Abre tu navegador y ve a `http://localhost:5173/register`
2. Completa el formulario de registro con los siguientes datos:
   - Email: `usuario_prueba@example.com`
   - Contraseña: `contraseña123`
   - Confirmar contraseña: `contraseña123`
   - Nombre: `Usuario`
   - Apellido: `Prueba`
3. Haz clic en el botón "Registrarse"
4. Deberías ver un mensaje de éxito indicando que se ha enviado un correo de activación

### 2. Verificación del correo de activación

#### Si configuraste el backend para mostrar correos en la consola:

1. Revisa la consola donde está ejecutándose el servidor de Django
2. Deberías ver el correo de activación con un enlace similar a:
   ```
   http://localhost:5173/#/activate/[uidb64]/[token]
   ```
3. Copia este enlace

#### Si configuraste el backend para enviar correos reales:

1. Revisa la bandeja de entrada del correo que proporcionaste durante el registro
2. Abre el correo con asunto "Activa tu cuenta en KandaBackend"
3. Haz clic en el botón "Activar mi cuenta" o copia el enlace proporcionado

### 3. Activación de la cuenta

1. Pega el enlace de activación en tu navegador o haz clic en el botón del correo
2. Deberías ser redirigido a una página que confirma que tu cuenta ha sido activada
3. Haz clic en "Ir a iniciar sesión"

### 4. Inicio de sesión

1. En la página de login, introduce el email y contraseña que usaste para registrarte
2. Haz clic en "Iniciar sesión"
3. Deberías ser redirigido al dashboard, lo que confirma que el flujo completo funciona correctamente

## Prueba de reenvío de correo de activación

1. Registra un nuevo usuario siguiendo los pasos anteriores
2. En lugar de activar la cuenta, ve a la página de login
3. Haz clic en el enlace "¿No has recibido el email de activación?"
4. Introduce el email del usuario que acabas de registrar
5. Haz clic en "Reenviar correo de activación"
6. Deberías recibir un nuevo correo de activación

## Prueba con Postman o curl

### Registro de usuario con curl

```bash
curl -X POST http://localhost:8000/api/api-register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"usuario_curl@example.com","password":"contraseña123","first_name":"Usuario","last_name":"Curl"}'
```

### Activación de cuenta con curl

```bash
# Reemplaza [uidb64] y [token] con los valores reales del correo
curl -X GET http://localhost:8000/api/api-activate/[uidb64]/[token]/
```

### Inicio de sesión con curl

```bash
curl -X POST http://localhost:8000/api/api-login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"usuario_curl@example.com","password":"contraseña123"}'
```

### Reenvío de correo de activación con curl

```bash
curl -X POST http://localhost:8000/api/api-resend-activation/ \
  -H "Content-Type: application/json" \
  -d '{"email":"usuario_curl@example.com"}'
```

## Solución de problemas

### El correo no se envía

1. Verifica que las credenciales en el archivo `.env` sean correctas
2. Si usas Gmail, asegúrate de haber generado una "contraseña de aplicación"
3. Verifica los logs de Django para ver si hay errores de SMTP
4. Prueba con el backend de consola para verificar que el correo se genera correctamente

### El enlace de activación no funciona

1. Asegúrate de que el enlace no esté truncado o modificado
2. Verifica que el token no haya expirado (2 días por defecto)
3. Comprueba que el usuario no haya sido eliminado de la base de datos

### Problemas de CORS

1. Verifica que la configuración de CORS en `settings.py` incluya el origen del frontend
2. Asegúrate de que el frontend esté haciendo las solicitudes al dominio correcto del backend

## Capturas de pantalla de logs

### Log de envío de correo en la consola

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Activa tu cuenta en KandaBackend
From: tu_correo@gmail.com
To: usuario_prueba@example.com
Date: Sun, 01 Jan 2023 12:00:00 -0000
Message-ID: <123456789.123456789@localhost>

...
<a href="http://localhost:5173/#/activate/MQ/abcdef123456">Activar mi cuenta</a>
...
```

### Log de activación exitosa

```
[01/Jan/2023 12:05:00] "GET /api/api-activate/MQ/abcdef123456/ HTTP/1.1" 200 52
```

### Log de inicio de sesión exitoso

```
[01/Jan/2023 12:10:00] "POST /api/api-login/ HTTP/1.1" 200 267
```