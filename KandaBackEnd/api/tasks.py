from celery import shared_task
import time
import logging
import openai
from django.conf import settings
from .models import CharacterProfile, ProcessingStatus
import datetime

# Configurar logger
logger = logging.getLogger(__name__)

# Plantilla de prompt para la generación de personajes
PROMPT_TEMPLATE = """
Crea un perfil detallado para un personaje ficticio con el nombre "{name}" y la siguiente descripción inicial: "{description}".

Genera información detallada en formato JSON para las siguientes categorías:

1. Personalidad: rasgos de carácter, valores, motivaciones, miedos, deseos.
2. Historia: origen, eventos importantes en su vida, traumas o momentos definitorios.
3. Apariencia: descripción física detallada, vestimenta habitual, características distintivas.
4. Relaciones: conexiones con otros personajes, familia, amigos, rivales, intereses románticos.
5. Habilidades: talentos especiales, conocimientos, poderes (si aplica), limitaciones.

El formato de respuesta debe ser un JSON válido con las siguientes claves: personality, background, appearance, relationships, abilities.
Cada sección debe ser detallada pero concisa.
"""

@shared_task(bind=True, max_retries=3, default_retry_delay=300)
def process_character_with_ai(self, character_id):
    """
    Tarea para procesar un perfil de personaje con la API de OpenAI.
    
    Args:
        character_id: ID del perfil de personaje a procesar
    
    Returns:
        dict: Resultado del procesamiento
    """
    try:
        # Obtener el perfil del personaje
        character = CharacterProfile.objects.get(id=character_id)
        
        # Actualizar estado a 'processing'
        character.processing_status.status = 'processing'
        character.processing_status.started_at = datetime.datetime.now()
        character.processing_status.attempts += 1
        character.processing_status.last_attempt = datetime.datetime.now()
        character.save()
        
        logger.info(f"Iniciando procesamiento de IA para personaje: {character.name} (ID: {character_id})")
        
        # Configurar cliente de OpenAI
        openai.api_key = settings.OPENAI_API_KEY
        
        # Preparar el prompt
        prompt = PROMPT_TEMPLATE.format(
            name=character.name,
            description=character.description
        )
        
        # Llamar a la API de OpenAI
        response = openai.ChatCompletion.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Eres un asistente especializado en crear perfiles detallados de personajes ficticios."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        # Extraer y procesar la respuesta
        ai_response = response.choices[0].message.content
        
        # Intentar parsear la respuesta como JSON
        import json
        try:
            character_data = json.loads(ai_response)
            
            # Si hay una versión anterior, guardarla en el historial
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
            
            # Actualizar el perfil con los datos generados
            character.personality = character_data.get('personality', {})
            character.background = character_data.get('background', {})
            character.appearance = character_data.get('appearance', {})
            character.relationships = character_data.get('relationships', [])
            character.abilities = character_data.get('abilities', [])
            
            # Actualizar estado a 'completed'
            character.processing_status.status = 'completed'
            character.processing_status.completed_at = datetime.datetime.now()
            character.save()
            
            logger.info(f"Procesamiento de IA completado para personaje: {character.name} (ID: {character_id})")
            
            return {
                'status': 'success',
                'character_id': str(character.id),
                'message': 'Perfil de personaje generado exitosamente'
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear respuesta JSON: {e}")
            raise self.retry(exc=e)
            
    except CharacterProfile.DoesNotExist:
        logger.error(f"Personaje no encontrado: {character_id}")
        return {
            'status': 'error',
            'message': f'Personaje no encontrado: {character_id}'
        }
        
    except Exception as e:
        logger.error(f"Error al procesar personaje {character_id}: {str(e)}")
        
        # Actualizar estado a 'failed'
        try:
            character = CharacterProfile.objects.get(id=character_id)
            character.processing_status.status = 'failed'
            character.processing_status.error_message = str(e)
            character.save()
        except Exception as inner_e:
            logger.error(f"Error al actualizar estado de error: {str(inner_e)}")
        
        # Reintentar si no se ha alcanzado el límite de reintentos
        raise self.retry(exc=e)