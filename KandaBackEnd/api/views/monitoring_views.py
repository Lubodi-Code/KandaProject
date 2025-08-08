from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from ..models import Character, User
import json
import logging
import datetime
import platform
import django

# Configurar logger
logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_statistics(request):
    """
    Endpoint para obtener estadísticas de personajes del usuario actual.
    """
    try:
        user = request.user
        
        # Obtener estadísticas
        stats = get_character_statistics(user.id)
        
        # Obtener personajes recientes
        recent_characters = CharacterProfile.objects(user=user).order_by('-created_at')[:5]
        recent_list = [{
            'id': str(char.id),
            'name': char.name,
            'created_at': char.created_at.isoformat(),
            'status': char.processing_status.status
        } for char in recent_characters]
        
        # Obtener personajes con errores
        failed_characters = CharacterProfile.objects(user=user, processing_status__status='failed')
        failed_list = [{
            'id': str(char.id),
            'name': char.name,
            'error': char.processing_status.error_message,
            'attempts': char.processing_status.attempts
        } for char in failed_characters]
        
        return JsonResponse({
            'status': 'success',
            'statistics': stats,
            'recent_characters': recent_list,
            'failed_characters': failed_list
        })
        
    except Exception as e:
        logger.error(f"Error al obtener estadísticas de usuario: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error al obtener estadísticas: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_statistics(request):
    """
    Endpoint para obtener estadísticas globales (solo para administradores).
    """
    try:
        # Obtener estadísticas globales
        global_stats = get_character_statistics()
        
        # Obtener estadísticas de usuarios
        user_count = User.objects.count()
        active_users = User.objects(is_active=True).count()
        inactive_users = user_count - active_users
        
        # Obtener usuarios con más personajes
        top_users = []
        for user in User.objects:
            character_count = CharacterProfile.objects(user=user).count()
            if character_count > 0:
                top_users.append({
                    'username': user.username,
                    'character_count': character_count,
                    'joined': user.date_joined.isoformat()
                })
        
        # Ordenar por cantidad de personajes (descendente)
        top_users.sort(key=lambda x: x['character_count'], reverse=True)
        top_users = top_users[:10]  # Limitar a los 10 principales
        
        # Obtener personajes recientes
        recent_characters = CharacterProfile.objects.order_by('-created_at')[:10]
        recent_list = [{
            'id': str(char.id),
            'name': char.name,
            'user': char.user.username,
            'created_at': char.created_at.isoformat(),
            'status': char.processing_status.status
        } for char in recent_characters]
        
        # Obtener personajes con errores recientes
        failed_characters = CharacterProfile.objects(processing_status__status='failed').order_by('-processing_status.last_attempt')[:10]
        failed_list = [{
            'id': str(char.id),
            'name': char.name,
            'user': char.user.username,
            'error': char.processing_status.error_message,
            'attempts': char.processing_status.attempts,
            'last_attempt': char.processing_status.last_attempt.isoformat() if char.processing_status.last_attempt else None
        } for char in failed_characters]
        
        return JsonResponse({
            'status': 'success',
            'global_statistics': global_stats,
            'user_statistics': {
                'total': user_count,
                'active': active_users,
                'inactive': inactive_users
            },
            'top_users': top_users,
            'recent_characters': recent_list,
            'failed_characters': failed_list
        })
        
    except Exception as e:
        logger.error(f"Error al obtener estadísticas de administrador: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error al obtener estadísticas: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def system_health(request):
    """
    Endpoint p+�blico para verificar el estado del sistema.
    No requiere autenticaci+�n.
    """
    try:
        # Informaci+�n del sistema
        system_info = {
            'status': 'operational',
            'timestamp': datetime.datetime.now().isoformat(),
            'system': {
                'python_version': platform.python_version(),
                'django_version': django.get_version(),
                'platform': platform.platform(),
            },
            'api_version': '1.0.0',
        }
        
        return JsonResponse(system_info)
        
    except Exception as e:
        logger.error(f"Error al verificar salud del sistema: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error interno del servidor: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def system_health_admin(request):
    """
    Endpoint para verificar el estado del sistema (solo para administradores).
    """
    try:
        # Verificar conexión a MongoDB
        mongo_status = 'ok'
        try:
            # Intentar una consulta simple
            User.objects.first()
        except Exception as e:
            mongo_status = f'error: {str(e)}'
        
        # Verificar estado de Celery (simplificado)
        celery_status = 'unknown'  # En una implementación real, se verificaría el estado de Celery
        
        # Verificar API de OpenAI
        openai_status = 'configured' if hasattr(request, 'openai_api_key') and request.openai_api_key else 'not configured'
        
        # Estadísticas de procesamiento
        processing_stats = {
            'pending': CharacterProfile.objects(processing_status__status='pending').count(),
            'processing': CharacterProfile.objects(processing_status__status='processing').count(),
            'completed': CharacterProfile.objects(processing_status__status='completed').count(),
            'failed': CharacterProfile.objects(processing_status__status='failed').count()
        }
        
        # Calcular tiempo promedio de procesamiento
        completed_characters = CharacterProfile.objects(
            processing_status__status='completed',
            processing_status__started_at__ne=None,
            processing_status__completed_at__ne=None
        )
        
        total_time = 0
        count = 0
        
        for char in completed_characters:
            if char.processing_status.started_at and char.processing_status.completed_at:
                processing_time = (char.processing_status.completed_at - char.processing_status.started_at).total_seconds()
                total_time += processing_time
                count += 1
        
        avg_processing_time = total_time / count if count > 0 else 0
        
        return JsonResponse({
            'status': 'success',
            'timestamp': datetime.datetime.now().isoformat(),
            'system_status': {
                'mongodb': mongo_status,
                'celery': celery_status,
                'openai_api': openai_status
            }
        })
        
    except Exception as e:
        logger.error(f"Error al verificar estado del sistema: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error al verificar estado del sistema: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)