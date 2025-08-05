from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CharacterProfile, User
from .tasks import process_character_with_ai
import json
import datetime
from bson import ObjectId
import logging

# Configurar logger
logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_character(request):
    """
    Endpoint para crear un nuevo perfil de personaje.
    
    Parámetros requeridos en el cuerpo de la solicitud:
    - name: Nombre del personaje
    - description: Descripción inicial del personaje
    - tags: Lista de etiquetas (opcional)
    """
    try:
        data = json.loads(request.body)
        
        # Validar datos requeridos
        if 'name' not in data or 'description' not in data:
            return JsonResponse({
                'status': 'error',
                'message': 'Se requieren los campos name y description'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener usuario actual
        user = request.user
        
        # Verificar límite de personajes
        character_count = CharacterProfile.objects(user=user).count()
        if character_count >= user.max_characters:
            return JsonResponse({
                'status': 'error',
                'message': f'Has alcanzado el límite de {user.max_characters} personajes'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar si ya existe un personaje con el mismo nombre para este usuario
        if CharacterProfile.objects(user=user, name=data['name']).first():
            return JsonResponse({
                'status': 'error',
                'message': f'Ya tienes un personaje con el nombre {data["name"]}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear nuevo perfil de personaje
        character = CharacterProfile(
            name=data['name'],
            description=data['description'],
            user=user,
            tags=data.get('tags', [])
        )
        character.save()
        
        # Iniciar tarea de procesamiento con IA en segundo plano
        process_character_with_ai.delay(str(character.id))
        
        return JsonResponse({
            'status': 'success',
            'message': 'Personaje creado exitosamente. El procesamiento con IA ha comenzado.',
            'character': {
                'id': str(character.id),
                'name': character.name,
                'description': character.description,
                'created_at': character.created_at.isoformat(),
                'processing_status': character.processing_status.status
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Error al crear personaje: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error al crear personaje: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_characters(request):
    """
    Endpoint para listar todos los personajes del usuario.
    
    Parámetros de consulta opcionales:
    - tag: Filtrar por etiqueta
    - status: Filtrar por estado de procesamiento
    - public: Filtrar por visibilidad (true/false)
    """
    try:
        user = request.user
        
        # Iniciar con la consulta base
        query = {'user': user}
        
        # Aplicar filtros opcionales
        tag = request.GET.get('tag')
        if tag:
            query['tags'] = tag
            
        status_filter = request.GET.get('status')
        if status_filter:
            query['processing_status.status'] = status_filter
            
        public = request.GET.get('public')
        if public is not None:
            query['is_public'] = public.lower() == 'true'
        
        # Ejecutar consulta
        characters = CharacterProfile.objects(**query)
        
        # Formatear resultados
        result = [{
            'id': str(char.id),
            'name': char.name,
            'description': char.description,
            'created_at': char.created_at.isoformat(),
            'updated_at': char.updated_at.isoformat(),
            'processing_status': char.processing_status.status,
            'is_public': char.is_public,
            'tags': char.tags,
            'version': char.version_number
        } for char in characters]
        
        return JsonResponse({
            'status': 'success',
            'count': len(result),
            'characters': result
        })
        
    except Exception as e:
        logger.error(f"Error al listar personajes: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error al listar personajes: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_character(request, character_id):
    """
    Endpoint para obtener los detalles de un personaje específico.
    
    Parámetros de ruta:
    - character_id: ID del personaje
    """
    try:
        user = request.user
        
        # Buscar el personaje
        character = CharacterProfile.objects.get(id=character_id)
        
        # Verificar propiedad o visibilidad pública
        if str(character.user.id) != str(user.id) and not character.is_public:
            return JsonResponse({
                'status': 'error',
                'message': 'No tienes permiso para ver este personaje'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Formatear respuesta
        result = {
            'id': str(character.id),
            'name': character.name,
            'description': character.description,
            'created_at': character.created_at.isoformat(),
            'updated_at': character.updated_at.isoformat(),
            'processing_status': {
                'status': character.processing_status.status,
                'started_at': character.processing_status.started_at.isoformat() if character.processing_status.started_at else None,
                'completed_at': character.processing_status.completed_at.isoformat() if character.processing_status.completed_at else None,
                'error_message': character.processing_status.error_message,
                'attempts': character.processing_status.attempts
            },
            'personality': character.personality,
            'background': character.background,
            'appearance': character.appearance,
            'relationships': character.relationships,
            'abilities': character.abilities,
            'is_public': character.is_public,
            'tags': character.tags,
            'version': character.version_number,
            'owner': character.user.username
        }
        
        return JsonResponse({
            'status': 'success',
            'character': result
        })
        
    except CharacterProfile.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Personaje no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Error al obtener personaje {character_id}: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error al obtener personaje: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_character(request, character_id):
    """
    Endpoint para actualizar un personaje existente.
    
    Parámetros de ruta:
    - character_id: ID del personaje
    """
    try:
        user = request.user
        data = json.loads(request.body)
        
        # Buscar el personaje
        character = CharacterProfile.objects.get(id=character_id)
        
        # Verificar propiedad
        if str(character.user.id) != str(user.id):
            return JsonResponse({
                'status': 'error',
                'message': 'No tienes permiso para modificar este personaje'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Actualizar campos permitidos
        if 'name' in data:
            # Verificar si ya existe otro personaje con el mismo nombre para este usuario
            existing = CharacterProfile.objects(user=user, name=data['name']).first()
            if existing and str(existing.id) != character_id:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Ya tienes un personaje con el nombre {data["name"]}'
                }, status=status.HTTP_400_BAD_REQUEST)
            character.name = data['name']
            
        if 'description' in data:
            character.description = data['description']
            
        if 'tags' in data:
            character.tags = data['tags']
            
        if 'is_public' in data:
            character.is_public = data['is_public']
        
        # Si se actualizó la descripción, reiniciar el procesamiento con IA
        if 'description' in data and data.get('regenerate', False):
            # Guardar versión actual en historial
            if character.personality or character.background or character.appearance:
                previous_version = {
                    'version': character.version_number,
                    'personality': character.personality,
                    'background': character.background,
                    'appearance': character.appearance,
                    'relationships': character.relationships,
                    'abilities': character.abilities,
                    'updated_at': character.updated_at.isoformat()
                }
                character.versions.append(previous_version)
                character.version_number += 1
            
            # Reiniciar estado de procesamiento
            character.processing_status.status = 'pending'
            character.processing_status.started_at = None
            character.processing_status.completed_at = None
            character.processing_status.error_message = ''
            character.processing_status.attempts = 0
            
            # Guardar cambios
            character.save()
            
            # Iniciar tarea de procesamiento con IA
            process_character_with_ai.delay(str(character.id))
            
            return JsonResponse({
                'status': 'success',
                'message': 'Personaje actualizado. El procesamiento con IA ha comenzado nuevamente.',
                'character_id': str(character.id)
            })
        else:
            # Guardar cambios sin regenerar
            character.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Personaje actualizado exitosamente',
                'character_id': str(character.id)
            })
        
    except CharacterProfile.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Personaje no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Error al actualizar personaje {character_id}: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error al actualizar personaje: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_character(request, character_id):
    """
    Endpoint para eliminar un personaje.
    
    Parámetros de ruta:
    - character_id: ID del personaje
    """
    try:
        user = request.user
        
        # Buscar el personaje
        character = CharacterProfile.objects.get(id=character_id)
        
        # Verificar propiedad
        if str(character.user.id) != str(user.id):
            return JsonResponse({
                'status': 'error',
                'message': 'No tienes permiso para eliminar este personaje'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Eliminar personaje
        character.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Personaje eliminado exitosamente'
        })
        
    except CharacterProfile.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Personaje no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Error al eliminar personaje {character_id}: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error al eliminar personaje: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_processing_status(request, character_id):
    """
    Endpoint para verificar el estado de procesamiento de un personaje.
    
    Parámetros de ruta:
    - character_id: ID del personaje
    """
    try:
        user = request.user
        
        # Buscar el personaje
        character = CharacterProfile.objects.get(id=character_id)
        
        # Verificar propiedad o visibilidad pública
        if str(character.user.id) != str(user.id) and not character.is_public:
            return JsonResponse({
                'status': 'error',
                'message': 'No tienes permiso para ver este personaje'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Formatear respuesta
        result = {
            'character_id': str(character.id),
            'name': character.name,
            'processing_status': {
                'status': character.processing_status.status,
                'started_at': character.processing_status.started_at.isoformat() if character.processing_status.started_at else None,
                'completed_at': character.processing_status.completed_at.isoformat() if character.processing_status.completed_at else None,
                'error_message': character.processing_status.error_message,
                'attempts': character.processing_status.attempts
            }
        }
        
        return JsonResponse({
            'status': 'success',
            'result': result
        })
        
    except CharacterProfile.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Personaje no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Error al obtener estado de procesamiento para {character_id}: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error al obtener estado de procesamiento: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def retry_processing(request, character_id):
    """
    Endpoint para reintentar el procesamiento de un personaje con IA.
    
    Parámetros de ruta:
    - character_id: ID del personaje
    """
    try:
        user = request.user
        
        # Buscar el personaje
        character = CharacterProfile.objects.get(id=character_id)
        
        # Verificar propiedad
        if str(character.user.id) != str(user.id):
            return JsonResponse({
                'status': 'error',
                'message': 'No tienes permiso para modificar este personaje'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Reiniciar estado de procesamiento
        character.processing_status.status = 'pending'
        character.processing_status.error_message = ''
        character.save()
        
        # Iniciar tarea de procesamiento con IA
        process_character_with_ai.delay(str(character.id))
        
        return JsonResponse({
            'status': 'success',
            'message': 'Procesamiento reiniciado exitosamente',
            'character_id': str(character.id)
        })
        
    except CharacterProfile.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Personaje no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Error al reintentar procesamiento para {character_id}: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error al reintentar procesamiento: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_character(request, character_id, format='json'):
    """
    Endpoint para exportar un personaje en diferentes formatos.
    
    Parámetros de ruta:
    - character_id: ID del personaje
    - format: Formato de exportación (json, txt, pdf)
    """
    try:
        user = request.user
        
        # Buscar el personaje
        character = CharacterProfile.objects.get(id=character_id)
        
        # Verificar propiedad o visibilidad pública
        if str(character.user.id) != str(user.id) and not character.is_public:
            return JsonResponse({
                'status': 'error',
                'message': 'No tienes permiso para exportar este personaje'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Verificar que el procesamiento esté completo
        if character.processing_status.status != 'completed':
            return JsonResponse({
                'status': 'error',
                'message': 'El personaje aún no ha sido procesado completamente'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Exportar según formato solicitado
        if format.lower() == 'json':
            # Convertir a diccionario
            character_data = character.to_dict()
            
            # Crear respuesta JSON para descarga
            response = HttpResponse(
                json.dumps(character_data, indent=4),
                content_type='application/json'
            )
            response['Content-Disposition'] = f'attachment; filename="{character.name.replace(" ", "_")}.json"'
            return response
            
        elif format.lower() == 'txt':
            # Crear versión de texto plano
            text_content = f"PERFIL DE PERSONAJE: {character.name}\n"
            text_content += f"===================={'=' * len(character.name)}\n\n"
            text_content += f"DESCRIPCIÓN:\n{character.description}\n\n"
            
            text_content += "PERSONALIDAD:\n"
            for key, value in character.personality.items():
                text_content += f"- {key}: {value}\n"
            text_content += "\n"
            
            text_content += "HISTORIA:\n"
            for key, value in character.background.items():
                text_content += f"- {key}: {value}\n"
            text_content += "\n"
            
            text_content += "APARIENCIA:\n"
            for key, value in character.appearance.items():
                text_content += f"- {key}: {value}\n"
            text_content += "\n"
            
            text_content += "RELACIONES:\n"
            for relation in character.relationships:
                for key, value in relation.items():
                    text_content += f"- {key}: {value}\n"
                text_content += "\n"
            
            text_content += "HABILIDADES:\n"
            for ability in character.abilities:
                for key, value in ability.items():
                    text_content += f"- {key}: {value}\n"
                text_content += "\n"
            
            text_content += f"\nCreado por: {character.user.username}\n"
            text_content += f"Fecha de creación: {character.created_at.strftime('%d/%m/%Y')}\n"
            text_content += f"Última actualización: {character.updated_at.strftime('%d/%m/%Y')}\n"
            
            # Crear respuesta para descarga
            response = HttpResponse(text_content, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="{character.name.replace(" ", "_")}.txt"'
            return response
            
        else:
            return JsonResponse({
                'status': 'error',
                'message': f'Formato de exportación no soportado: {format}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except CharacterProfile.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Personaje no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Error al exportar personaje {character_id}: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error al exportar personaje: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)