import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from functools import wraps

from .models import TestModel, User
from .forms import UserRegistrationForm, UserLoginForm
from .tokens import account_activation_token
from mongoengine.errors import ValidationError, NotUniqueError
from pymongo.errors import ConnectionFailure

# Create your views here.


def test_connection(request):
    """
    Una vista para probar la conexión a MongoDB.
    Intenta una operación de lectura simple para verificar que todo funciona.
    """
    try:
        # Intentamos contar los documentos en la colección.
        # Esta es una operación de bajo impacto que fallará si no hay conexión.
        count = TestModel.objects.count()
        return JsonResponse({
            "status": "success",
            "message": f"Conexión a MongoDB exitosa. Se encontraron {count} documentos en la colección 'test_model'."
        })
    except ConnectionFailure as e:
        # Capturamos un error de conexión específico para dar un mensaje más claro.
        return JsonResponse({"status": "error", "message": "Fallo de conexión a MongoDB.", "details": str(e)}, status=500)
    except Exception as e:
        # Capturamos cualquier excepción, que usualmente indica un problema de conexión o autenticación.
        return JsonResponse({"status": "error", "message": "No se pudo conectar a MongoDB.", "details": str(e)}, status=500)


def register(request):
    """
    Vista para el registro de nuevos usuarios.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Crear un nuevo usuario pero no activarlo todavía
                user = User(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1'],
                    is_active=False
                )
                user.save()
                
                # Enviar correo de activación
                send_activation_email(request, user)
                
                messages.success(request, 'Tu cuenta ha sido creada. Por favor, revisa tu correo para activarla.')
                return redirect('login')
            except NotUniqueError:
                messages.error(request, 'Ya existe un usuario con ese nombre de usuario o correo electrónico.')
            except Exception as e:
                messages.error(request, f'Error al crear la cuenta: {str(e)}')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'api/register.html', {'form': form})


def send_activation_email(request, user):
    """
    Envía un correo electrónico con un enlace de activación al usuario.
    """
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
    })
    
    # Enviar el correo
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.content_subtype = 'html'  # Para enviar contenido HTML
    email.send()


def activate_account(request, uidb64, token):
    """
    Vista para activar la cuenta de un usuario mediante el token enviado por correo.
    """
    try:
        # Decodificar el ID del usuario
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    # Verificar que el usuario existe y el token es válido
    if user is not None and account_activation_token.check_token(user, token):
        # Activar la cuenta
        user.is_active = True
        user.save()
        messages.success(request, 'Tu cuenta ha sido activada correctamente. Ya puedes iniciar sesión.')
        return redirect('login')
    else:
        return render(request, 'api/activation_invalid.html', {
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS
        })


def user_login(request):
    """
    Vista para el inicio de sesión de usuarios.
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Autenticar al usuario
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    # Implementación personalizada de login para MongoEngine
                    # En lugar de usar login(request, user), hacemos esto manualmente
                    request.session['_auth_user_id'] = str(user.id)
                    request.session['_auth_user_backend'] = 'api.auth_backends.MongoEngineBackend'
                    
                    messages.success(request, f'Bienvenido, {user.username}!')
                    return redirect('dashboard')  # Redirigir a la página principal después del login
                else:
                    messages.error(request, 'Tu cuenta no está activada. Por favor, revisa tu correo.')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = UserLoginForm()
    
    return render(request, 'api/login.html', {'form': form})


def user_logout(request):
    """
    Vista para cerrar sesión.
    """
    # Implementación personalizada de logout para MongoEngine
    # Limpiamos las claves de sesión que establecimos en el login
    if '_auth_user_id' in request.session:
        del request.session['_auth_user_id']
    if '_auth_user_backend' in request.session:
        del request.session['_auth_user_backend']
    request.session.flush()
    
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')


def mongo_login_required(view_func):
    """
    Decorador personalizado para verificar si el usuario está autenticado.
    Similar a login_required de Django pero compatible con nuestro sistema MongoEngine.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        if '_auth_user_id' not in request.session:
            # Redirigir al login si no está autenticado
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

@mongo_login_required
def dashboard(request):
    """
    Vista del panel de control, solo accesible para usuarios autenticados.
    """
    # Obtener el usuario actual desde la sesión
    user_id = request.session.get('_auth_user_id')
    user = User.objects.get(id=user_id) if user_id else None
    
    return render(request, 'api/dashboard.html', {'user': user})


def resend_activation(request):
    """
    Vista para reenviar el correo de activación.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                send_activation_email(request, user)
                messages.success(request, 'Se ha enviado un nuevo correo de activación.')
            else:
                messages.info(request, 'Esta cuenta ya está activada. Puedes iniciar sesión.')
        except User.DoesNotExist:
            # No informamos si el correo existe o no por seguridad
            messages.success(request, 'Si el correo existe en nuestra base de datos, recibirás un enlace de activación.')
    
    return render(request, 'api/resend_activation.html')


@csrf_exempt  # Usar solo para desarrollo/pruebas de API sin sesión.
def test_model_view(request):
    """
    Vista para crear (POST) y listar (GET) objetos TestModel.
    """
    if request.method == 'GET':
        items = TestModel.objects()
        # Convertir los objetos a una lista de diccionarios para la respuesta JSON
        items_list = []
        for item in items:
            item_dict = item.to_mongo().to_dict()
            item_dict['_id'] = str(item_dict['_id']) # Convertir ObjectId a string
            items_list.append(item_dict)
        return JsonResponse(items_list, safe=False)

    if request.method == 'POST':
        try:
            # Cargar los datos del cuerpo de la petición
            data = json.loads(request.body)
            name = data.get('name')

            if not name:
                return JsonResponse({"status": "error", "message": "El campo 'name' es requerido."}, status=400)

            # Crear y guardar el nuevo objeto
            new_item = TestModel(name=name)
            new_item.save()

            # Preparar la respuesta
            response_data = new_item.to_mongo().to_dict()
            response_data['_id'] = str(response_data['_id'])

            return JsonResponse({"status": "success", "data": response_data}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Cuerpo de la petición no es un JSON válido."}, status=400)
        except ValidationError as e:
            return JsonResponse({"status": "error", "message": "Datos inválidos.", "details": e.to_dict()}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": "Ocurrió un error inesperado.", "details": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": f"Método {request.method} no permitido."}, status=405)
