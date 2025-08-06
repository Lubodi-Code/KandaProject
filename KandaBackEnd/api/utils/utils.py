import logging
import openai
from django.conf import settings
import json
from ..models.documents import CharacterProfile

# Configurar logger
logger = logging.getLogger(__name__)

def initialize_openai_client():
    """
    Inicializa y configura el cliente de OpenAI.
    
    Returns:
        bool: True si la inicialización fue exitosa, False en caso contrario
    """
    try:
        # Verificar que la clave API esté configurada
        if not settings.OPENAI_API_KEY:
            logger.error("La clave API de OpenAI no está configurada en las variables de entorno")
            return False
        
        # Configurar cliente
        openai.api_key = settings.OPENAI_API_KEY
        return True
    except Exception as e:
        logger.error(f"Error al inicializar cliente de OpenAI: {str(e)}")
        return False


def generate_character_profile(name, description):
    """
    Genera un perfil de personaje utilizando la API de OpenAI.
    
    Args:
        name (str): Nombre del personaje
        description (str): Descripción inicial del personaje
    
    Returns:
        dict: Datos del perfil generado o None si ocurre un error
    """
    try:
        # Inicializar cliente
        if not initialize_openai_client():
            return None
        
        # Plantilla de prompt
        prompt = f"""
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
        try:
            character_data = json.loads(ai_response)
            return character_data
        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear respuesta JSON: {e}")
            return None
            
    except Exception as e:
        logger.error(f"Error al generar perfil de personaje: {str(e)}")
        return None


def get_character_statistics(user_id=None):
    """
    Obtiene estadísticas sobre los personajes en la base de datos.
    
    Args:
        user_id (str, optional): ID del usuario para filtrar estadísticas
    
    Returns:
        dict: Estadísticas de personajes
    """
    try:
        # Iniciar con la consulta base
        query = {}
        if user_id:
            query['user'] = user_id
        
        # Obtener conteos por estado
        total_characters = CharacterProfile.objects(**query).count()
        pending_characters = CharacterProfile.objects(**query, processing_status__status='pending').count()
        processing_characters = CharacterProfile.objects(**query, processing_status__status='processing').count()
        completed_characters = CharacterProfile.objects(**query, processing_status__status='completed').count()
        failed_characters = CharacterProfile.objects(**query, processing_status__status='failed').count()
        
        # Obtener conteos por visibilidad
        public_characters = CharacterProfile.objects(**query, is_public=True).count()
        private_characters = CharacterProfile.objects(**query, is_public=False).count()
        
        # Calcular porcentajes
        completion_rate = (completed_characters / total_characters * 100) if total_characters > 0 else 0
        failure_rate = (failed_characters / total_characters * 100) if total_characters > 0 else 0
        
        return {
            'total': total_characters,
            'by_status': {
                'pending': pending_characters,
                'processing': processing_characters,
                'completed': completed_characters,
                'failed': failed_characters
            },
            'by_visibility': {
                'public': public_characters,
                'private': private_characters
            },
            'rates': {
                'completion': round(completion_rate, 2),
                'failure': round(failure_rate, 2)
            }
        }
        
    except Exception as e:
        logger.error(f"Error al obtener estadísticas de personajes: {str(e)}")
        return {
            'total': 0,
            'by_status': {'pending': 0, 'processing': 0, 'completed': 0, 'failed': 0},
            'by_visibility': {'public': 0, 'private': 0},
            'rates': {'completion': 0, 'failure': 0}
        }