# views.py (CORREGIDO)
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import secrets
from datetime import datetime, timedelta
from mongoengine.errors import DoesNotExist, NotUniqueError
import logging

from ..models import User

# Configurar logging
logger = logging.getLogger(__name__)

# Almacén temporal de tokens (en producción debería ser Redis o MongoDB)
token_store = {}

@csrf_exempt
def api_login(request):
    """Vista de API para el inicio de sesión."""
    if request.method != 'POST':
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({"error": "Email y contraseña son requeridos"}, status=400)
        
        # Buscar usuario por email usando MongoEngine
        try:
            user = User.objects.get(email=email)
            logger.info(f"Usuario encontrado: {user.email}")
            
            # Verificar contraseña
            if not user.check_password(password):
                logger.warning(f"Contraseña incorrecta para usuario: {email}")
                return JsonResponse({"error": "Credenciales inválidas"}, status=401)
                
        except DoesNotExist:
            logger.warning(f"Usuario no encontrado: {email}")
            return JsonResponse({"error": "Credenciales inválidas"}, status=401)
        
        # Verificar si la cuenta está activa
        if not user.is_active:
            return JsonResponse({"error": "Cuenta no activada"}, status=403)
        
        # Actualizar last_login
        user.last_login = datetime.now()
        user.save()
        
        # Generar token
        token = secrets.token_hex(32)
        expires_in = 86400  # 24 horas
        
        token_store[token] = {
            'user_id': str(user.id),
            'expires': datetime.now() + timedelta(seconds=expires_in)
        }
        
        logger.info(f"Login exitoso para usuario: {email}")
        
        return JsonResponse({
            "token": token,
            "expires_in": expires_in,
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email
            }
        })
            
    except json.JSONDecodeError:
        return JsonResponse({"error": "Formato JSON inválido"}, status=400)
    except Exception as e:
        logger.error(f"Error en api_login: {str(e)}")
        return JsonResponse({"error": "Error interno del servidor"}, status=500)

@csrf_exempt
def api_register(request):
    """Vista de API para el registro de usuarios."""
    if request.method != 'POST':
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        
        # Validar datos requeridos
        if not email or not password:
            return JsonResponse({"error": "Email y contraseña son requeridos"}, status=400)
        
        # Validar formato de email básico
        if '@' not in email:
            return JsonResponse({"error": "Formato de email inválido"}, status=400)
        
        # Crear username a partir del email si no se proporciona
        username = data.get('username', email.split('@')[0])
        
        try:
            # Crear usuario (MongoEngine manejará la verificación de unicidad)
            user = User(
                username=username,
                email=email,
                password=password,  # Se hasheará automáticamente en save()
                is_active=False  # Usuario inactivo hasta confirmar email
            )
            
            # Asignar campos opcionales solo si existen en el modelo
            if hasattr(user, 'first_name'):
                user.first_name = first_name
            if hasattr(user, 'last_name'):
                user.last_name = last_name

            user.save()
            
            # Generar y enviar email de activación
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes
            from django.core.mail import EmailMessage
            from django.template.loader import render_to_string
            from django.conf import settings
            from .tokens import account_activation_token
            
            # Generar token único para este usuario
            token = account_activation_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(str(user.id)))
            
            # Construir el mensaje de correo
            mail_subject = 'Activa tu cuenta en KandaBackend'
            message = render_to_string('api/activation_email.html', {
                'user': user,
                'domain': request.get_host(),
                'uid': uid,
                'token': token,
                'protocol': 'https' if request.is_secure() else 'http',
                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                'frontend_url': settings.FRONTEND_URL,
            })
            
            # Enviar el correo
            email_obj = EmailMessage(mail_subject, message, to=[user.email])
            email_obj.content_subtype = 'html'  # Para enviar contenido HTML
            email_obj.send()
            
            logger.info(f"Usuario registrado exitosamente y correo de activación enviado: {email}")
            
            return JsonResponse({
                "message": "Usuario registrado exitosamente. Se ha enviado un correo de activación.",
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email
                }
            }, status=201)
            
        except NotUniqueError as e:
            # MongoEngine lanza esta excepción si hay duplicados
            if 'email' in str(e):
                return JsonResponse({"error": "Este email ya está registrado"}, status=400)
            elif 'username' in str(e):
                return JsonResponse({"error": "Este nombre de usuario ya está en uso"}, status=400)
            else:
                return JsonResponse({"error": "Ya existe un usuario con estos datos"}, status=400)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Formato JSON inválido"}, status=400)
    except Exception as e:
        logger.error(f"Error en api_register: {str(e)}")
        return JsonResponse({"error": "Error interno del servidor"}, status=500)

@csrf_exempt
def api_dashboard(request):
    """Vista de API para obtener datos del dashboard."""
    # Verificar token de autenticación
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Token '):
        return JsonResponse({"error": "Token de autenticación requerido"}, status=401)
    
    token = auth_header.split(' ')[1]
    token_data = token_store.get(token)
    
    if not token_data or token_data['expires'] < datetime.now():
        return JsonResponse({"error": "Token inválido o expirado"}, status=401)
    
    try:
        # Usar MongoEngine para buscar por ObjectId
        from bson import ObjectId
        user = User.objects.get(id=ObjectId(token_data['user_id']))
        
        # Construir el diccionario de datos del usuario de forma segura
        user_data = {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "date_joined": user.date_joined.isoformat() if user.date_joined else None
        }
        
        # Añadir campos opcionales solo si existen en el modelo para evitar errores
        if hasattr(user, 'first_name'):
            user_data['first_name'] = user.first_name
        if hasattr(user, 'last_name'):
            user_data['last_name'] = user.last_name

        return JsonResponse({
            "user": user_data,
            "message": "Bienvenido a tu dashboard"
        })
    except DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)
    except Exception as e:
        logger.error(f"Error en api_dashboard: {str(e)}")
        return JsonResponse({"error": "Error interno del servidor"}, status=500)

@csrf_exempt
def api_activate_account(request, uidb64, token):
    """Vista de API para activar la cuenta de un usuario mediante el token enviado por correo."""
    try:
        # Decodificar el ID del usuario
        from django.utils.http import urlsafe_base64_decode
        from django.utils.encoding import force_str
        from .tokens import account_activation_token
        
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        logger.warning(f"Intento de activación con ID de usuario inválido: {uidb64}")
        return JsonResponse({"error": "Enlace de activación inválido"}, status=400)
    
    # Verificar que el usuario existe y el token es válido
    if user is not None and account_activation_token.check_token(user, token):
        # Activar la cuenta si no está ya activada
        if not user.is_active:
            user.is_active = True
            user.save()
            logger.info(f"Cuenta activada exitosamente para usuario: {user.email}")
            return JsonResponse({"message": "Tu cuenta ha sido activada correctamente. Ya puedes iniciar sesión."}, status=200)
        else:
            logger.info(f"Intento de activación para cuenta ya activa: {user.email}")
            return JsonResponse({"message": "Esta cuenta ya está activada. Puedes iniciar sesión."}, status=200)
    else:
        logger.warning(f"Intento de activación con token inválido para usuario: {uidb64}")
        return JsonResponse({"error": "Enlace de activación inválido o expirado"}, status=400)

@csrf_exempt
def api_resend_activation(request):
    """Vista para reenviar el correo de activación."""
    if request.method != 'POST':
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get('email')

        if not email:
            return JsonResponse({"error": "Email es requerido"}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Para evitar la enumeración de usuarios, siempre devolvemos un mensaje genérico.
            logger.warning(f"Intento de reenvío de activación para email no registrado: {email}")
            return JsonResponse({"message": "Si una cuenta con este email existe y no está activada, se ha enviado un nuevo correo."}, status=200)

        if user.is_active:
            logger.info(f"Intento de reenvío de activación para cuenta ya activa: {email}")
            return JsonResponse({"error": "Esta cuenta ya ha sido activada."}, status=400)

        # Generar y enviar email de activación
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.core.mail import EmailMessage
        from django.template.loader import render_to_string
        from django.conf import settings
        from .tokens import account_activation_token
        
        # Generar token único para este usuario
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(str(user.id)))
        
        # Construir el mensaje de correo
        mail_subject = 'Activa tu cuenta en KandaBackend'
        message = render_to_string('api/activation_email.html', {
            'user': user,
            'domain': request.get_host(),
            'uid': uid,
            'token': token,
            'protocol': 'https' if request.is_secure() else 'http',
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            'frontend_url': settings.FRONTEND_URL,
        })
        
        # Enviar el correo
        email_obj = EmailMessage(mail_subject, message, to=[user.email])
        email_obj.content_subtype = 'html'  # Para enviar contenido HTML
        email_obj.send()
        
        logger.info(f"Reenviando email de activación para: {email}")
        
        return JsonResponse({"message": "Se ha enviado un nuevo correo de activación a tu dirección de email."}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Formato JSON inválido"}, status=400)
    except Exception as e:
        logger.error(f"Error en api_resend_activation: {str(e)}")
        return JsonResponse({"error": "Error interno del servidor"}, status=500)
