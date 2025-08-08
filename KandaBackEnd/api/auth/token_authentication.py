from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime, timedelta

class CustomTokenAuthentication(BaseAuthentication):
    """
    Autenticaci+¦n personalizada basada en tokens para usar con nuestro almac+®n personalizado.
    """
    keyword = 'Token'
    
    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '').split()
        
        if not auth or auth[0].lower() != self.keyword.lower():
            return None
            
        if len(auth) == 1:
            msg = _('Token de autorizaci+¦n inv+ílido.')
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Token de autorizaci+¦n inv+ílido. No debe contener espacios.')
            raise AuthenticationFailed(msg)
            
        return self.authenticate_credentials(auth[1])
    
    def authenticate_credentials(self, key):
        """
        Autentica por credenciales de token utilizando nuestro almac+®n personalizado.
        """
        # Importamos aqu+¡ para evitar problemas de importaci+¦n circular
        from ..views.api_views import token_store
        
        # Buscar el token en nuestro almac+®n temporal
        token_data = token_store.get(key)
        
        if not token_data:
            raise AuthenticationFailed(_('Token inv+ílido.'))
        
        # Verificar si el token ha expirado
        # Convertir token_data['expires'] a timezone-aware si no lo es
        expires_time = token_data['expires']
        if expires_time.tzinfo is None:
            expires_time = timezone.make_aware(expires_time)
        
        current_time = timezone.now()
        
        if expires_time < current_time:
            # Limpiar el token expirado
            if key in token_store:
                del token_store[key]
            raise AuthenticationFailed(_('Token expirado.'))
        
        # Obtener el usuario asociado al token
        from ..models import User
        try:
            from bson import ObjectId
            user = User.objects.get(id=ObjectId(token_data['user_id']))
        except User.DoesNotExist:
            raise AuthenticationFailed(_('Usuario no encontrado.'))
        
        if not user.is_active:
            raise AuthenticationFailed(_('Usuario inactivo o eliminado.'))
        
        return (user, key)
        
    def authenticate_header(self, request):
        return self.keyword
