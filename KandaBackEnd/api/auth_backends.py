from django.contrib.auth.backends import BaseBackend
from .models import User
import datetime

class MongoEngineBackend(BaseBackend):
    """
    Backend de autenticación personalizado para usar con MongoEngine.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica un usuario usando username/password.
        """
        if username is None or password is None:
            return None
            
        try:
            # Intentamos encontrar al usuario por username
            user = User.objects.get(username=username)
            
            # Verificamos que la cuenta esté activa y la contraseña sea correcta
            if user.is_active and user.check_password(password):
                # Actualizamos la fecha del último login
                user.last_login = datetime.datetime.now()
                user.save()
                return user
        except User.DoesNotExist:
            # También podemos intentar buscar por email
            try:
                user = User.objects.get(email=username)
                if user.is_active and user.check_password(password):
                    user.last_login = datetime.datetime.now()
                    user.save()
                    return user
            except User.DoesNotExist:
                return None
        
        return None
    
    def get_user(self, user_id):
        """
        Recupera un usuario por su ID.
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None