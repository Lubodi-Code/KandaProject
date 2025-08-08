from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

# Importar el almac+®n de tokens
from ..views.api_views import token_store

# Configurar logging
logger = logging.getLogger(__name__)

@csrf_exempt
def api_logout(request):
    """Vista de API para cerrar sesi+¦n."""
    if request.method != 'POST':
        return JsonResponse({"error": "M+®todo no permitido"}, status=405)
    
    # En una implementaci+¦n basada en tokens, el logout es principalmente
    # un proceso del lado del cliente donde se elimina el token.
    # Aqu+¡ solo registramos el evento y respondemos con +®xito.
    
    # Verificar si hay token para identificar al usuario
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Token '):
        token = auth_header.split(' ')[1]
        # Eliminar token del almac+®n (si existe)
        if token in token_store:
            del token_store[token]
            logger.info(f"Token invalidado durante logout")
    
    return JsonResponse({"message": "Sesi+¦n cerrada con +®xito"})
