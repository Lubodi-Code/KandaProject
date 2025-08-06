from .models import User

class MongoAuthMiddleware:
    """
    Middleware personalizado para agregar el usuario actual al contexto de la solicitud.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Antes de procesar la vista
        user_id = request.session.get('_auth_user_id')
        
        # Agregar un atributo user a la solicitud
        if user_id:
            try:
                request.user = User.objects.get(id=user_id)
                request.user.is_authenticated = True
            except User.DoesNotExist:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
        
        response = self.get_response(request)
        
        # Después de procesar la vista
        return response


class AnonymousUser:
    """
    Clase para representar a un usuario anónimo.
    """
    is_authenticated = False
    username = 'AnonymousUser'
    
    def __str__(self):
        return 'AnonymousUser'