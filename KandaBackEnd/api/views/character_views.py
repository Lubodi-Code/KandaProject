from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
import logging

from ..models import Character
from ..serializers.character import CharacterSerializer
from ..utils.character_ai import generate_ai_filter
from ..auth.token_authentication import CustomTokenAuthentication

# Configurar logger
logger = logging.getLogger(__name__)


class CharacterViewSet(viewsets.ViewSet):
    """API endpoint for CRUD operations on characters using MongoEngine."""

    permission_classes = [AllowAny]  # Permitir acceso para detectar errores espec+°ficos
    authentication_classes = [CustomTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        # Si el usuario no est+Ì autenticado, devolver lista vac+°a
        if not self.request.user.is_authenticated:
            return Character.objects.none()
        return Character.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        # Si el usuario no est+Ì autenticado, devolver error espec+°fico
        if not request.user.is_authenticated:
            return Response(
                {"error": "Autenticaci+¶n requerida para acceder a los personajes"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Obtener personajes del usuario actual
        characters = Character.objects.filter(user=request.user)
        serializer = CharacterSerializer(characters, many=True, context={'request': request})
        return Response(serializer.data)
        
    def retrieve(self, request, pk=None, *args, **kwargs):
        # Si el usuario no est+Ì autenticado, devolver error espec+°fico
        if not request.user.is_authenticated:
            return Response(
                {"error": "Autenticaci+¶n requerida para acceder a los personajes"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            from bson import ObjectId
            character = Character.objects.get(id=ObjectId(pk), user=request.user)
            serializer = CharacterSerializer(character, context={'request': request})
            return Response(serializer.data)
        except Character.DoesNotExist:
            return Response(
                {"error": "Personaje no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error al obtener el personaje: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request, *args, **kwargs):
        # Si el usuario no est+Ì autenticado, devolver error espec+°fico
        if not request.user.is_authenticated:
            return Response(
                {"error": "Autenticaci+¶n requerida para crear personajes"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Logging detallado para debug
        logger.info(f"Character create request from user: {request.user}")
        logger.info(f"Request data: {request.data}")
        
        serializer = CharacterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            character = serializer.save()
            # Generar datos de IA si es necesario
            try:
                ai_data = generate_ai_filter(character)
                if ai_data:
                    character.aiFilter.update(ai_data)
                    character.save()
            except Exception as e:
                logger.warning(f"Error generando AI filter: {str(e)}")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Logging detallado de errores de validaci+¶n
        logger.error(f"Character creation validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        # Si el usuario no est+Ì autenticado, devolver error espec+°fico
        if not request.user.is_authenticated:
            return Response(
                {"error": "Autenticaci+¶n requerida para actualizar personajes"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            from bson import ObjectId
            character = Character.objects.get(id=ObjectId(pk), user=request.user)
            serializer = CharacterSerializer(character, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                updated_character = serializer.save()
                # Generar datos de IA si es necesario
                try:
                    ai_data = generate_ai_filter(updated_character)
                    if ai_data:
                        updated_character.aiFilter.update(ai_data)
                        updated_character.save()
                except Exception as e:
                    logger.warning(f"Error generando AI filter: {str(e)}")
                
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Character.DoesNotExist:
            return Response(
                {"error": "Personaje no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error al actualizar el personaje: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk=None, *args, **kwargs):
        # Si el usuario no est+Ì autenticado, devolver error espec+°fico
        if not request.user.is_authenticated:
            return Response(
                {"error": "Autenticaci+¶n requerida para eliminar personajes"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            from bson import ObjectId
            character = Character.objects.get(id=ObjectId(pk), user=request.user)
            character.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Character.DoesNotExist:
            return Response(
                {"error": "Personaje no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error al eliminar el personaje: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomTokenAuthentication, SessionAuthentication])
def create_default_character(request):
    """Create a default character for the authenticated user."""
    try:
        character = Character.create_default(user=request.user)
        try:
            ai_data = generate_ai_filter(character)
            if ai_data:
                character.aiFilter.update(ai_data)
                character.save()
        except Exception as e:
            logger.warning(f"Error generando AI filter para personaje por defecto: {str(e)}")
        
        serializer = CharacterSerializer(character, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error creando personaje por defecto: {str(e)}")
        return Response(
            {"error": f"Error al crear personaje por defecto: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomTokenAuthentication, SessionAuthentication])
def evaluate_character(request):
    """Evaluate a character with AI without saving it to the database."""
    try:
        logger.info(f"Solicitud de evaluaci+¶n desde usuario: {request.user}")
        
        # Parsear los datos del request
        import json
        
        # Si el request tiene .data (DRF), usarlo. Si no, parsear el body.
        if hasattr(request, 'data') and request.data:
            data = request.data
        else:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return Response(
                    {"error": "Datos JSON inv+Ìlidos"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Log de debug para ver qu+Æ datos llegan
        logger.info(f"Datos recibidos para evaluaci+¶n: {data}")
        
        # Validar que tengamos al menos un nombre
        if not data.get('name'):
            return Response(
                {"error": "El nombre del personaje es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create a temporary Character object (don't save to database)
        # Solo usar campos que existen en el modelo Character
        temp_character = Character(
            user=request.user,
            name=data.get('name', ''),
            age=data.get('age', 0),
            archetype=data.get('archetype', 'Aventurero'),  # Valor por defecto
            gender=data.get('gender', ''),
            # Mapear los campos del frontend a los del modelo
            physical_traits=[data.get('physical_description', '')] if data.get('physical_description') else [],
            personality_traits=[data.get('personality', '')] if data.get('personality') else [],
            weaknesses=[data.get('weaknesses', '')] if data.get('weaknesses') else [],
            background=data.get('history', ''),
            special_abilities=data.get('special_abilities', ''),
            goals=data.get('goals', '')
        )
        
        # Generate AI suggestions
        try:
            ai_data = generate_ai_filter(temp_character)
            if not ai_data:
                return Response(
                    {"error": "No se pudieron generar sugerencias de IA"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Formatear respuesta mejorada para el frontend con el nuevo sistema
            evaluation_result = {
                "overall_score": ai_data.get('overall_score', 80) // 10,  # Convertir a escala 1-10
                "quality_score": ai_data.get('quality_score', 8),
                "balance_score": ai_data.get('balance_score', 8),
                "quality_category": ai_data.get('overall_category', 'Bueno'),
                "comments": ai_data.get('analysis', 'Personaje evaluado exitosamente'),
                "suggestions": ai_data.get('suggestions', 'Contin+¶a desarrollando el personaje'),
                
                # Informaci+¶n detallada de fortalezas y debilidades
                "suggested_improvements": {
                    "strengths": '; '.join(ai_data.get('strengths', [])) if ai_data.get('strengths') else 'Sin fortalezas espec+°ficas generadas',
                    "weaknesses": '; '.join(ai_data.get('flaws', [])) if ai_data.get('flaws') else 'Sin debilidades espec+°ficas generadas',
                    "history": ai_data.get('background', data.get('history', '')),
                    "personality": data.get('personality', '')
                },
                
                # Campos separados para compatibilidad con frontend existente
                "suggested_strengths": '; '.join(ai_data.get('strengths', [])) if ai_data.get('strengths') else '',
                "suggested_weaknesses": '; '.join(ai_data.get('flaws', [])) if ai_data.get('flaws') else '',
                "suggested_history": ai_data.get('background', data.get('history', '')),
                "suggested_personality": data.get('personality', ''),
                
                # Informaci+¶n adicional del nuevo sistema
                "depth_analysis": ai_data.get('depth_analysis', {}),
                "abilities_balance": ai_data.get('abilities_balance', {}),
                "detailed_scores": {
                    "development": ai_data.get('depth_analysis', {}).get('score', 0),
                    "abilities_balance": ai_data.get('abilities_balance', {}).get('balance_score', 5),
                    "creativity": ai_data.get('quality_score', 7),
                    "narrative_potential": ai_data.get('balance_score', 7)
                },
                
                "success": True
            }
            
            return Response(evaluation_result)
        except Exception as e:
            logger.error(f"Error generando evaluaci+¶n de IA: {str(e)}")
            return Response(
                {"error": f"Error al evaluar personaje con IA: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        logger.error(f"Error en evaluate_character: {str(e)}")
        return Response(
            {"error": f"Error al procesar la solicitud: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomTokenAuthentication, SessionAuthentication])
def generate_background(request):
    """Generate a character background using AI."""
    
    try:
        logger.info(f"Solicitud de generaci+¶n de trasfondo desde usuario: {request.user}")
        
        # Importar aqu+° para evitar importaci+¶n circular
        from ..utils.character_ai import generate_character_background
        
        character_data = request.data
        
        # Validaci+¶n b+Ìsica
        if not character_data:
            return Response(
                {"error": "Se requieren datos del personaje para generar el trasfondo"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Generar trasfondo con IA
        try:
            background_result = generate_character_background(character_data)
            
            if background_result.get('success'):
                return Response({
                    "background": background_result.get('background', ''),
                    "success": True,
                    "mock": background_result.get('mock', False)
                })
            else:
                return Response(
                    {"error": "No se pudo generar el trasfondo"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except Exception as ai_error:
            logger.error(f"Error generando trasfondo con IA: {str(ai_error)}")
            return Response(
                {"error": f"Error al generar trasfondo con IA: {str(ai_error)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        logger.error(f"Error en generate_background: {str(e)}")
        return Response(
            {"error": f"Error al procesar la solicitud: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def create_character_test(request):
    """
    Endpoint temporal para testing de creaci+¶n de personajes sin autenticaci+¶n.
    SOLO PARA DESARROLLO - ELIMINAR EN PRODUCCI+ÙN
    """
    print("=== TESTING CHARACTER CREATION ENDPOINT CALLED ===")
    print("Request method:", request.method)
    print("Request content type:", request.content_type)
    print("Request path:", request.path)
    print("Full URL:", request.build_absolute_uri())
    
    try:
        # Solo usar request.data para DRF, NO acceder a request.body despu+Æs
        raw_data = request.data.copy() if request.data else {}
        
        print("Raw request data:", raw_data)
        
        # Verificar si los datos est+Ìn anidados dentro de 'data'
        if 'data' in raw_data and isinstance(raw_data['data'], dict):
            character_data = raw_data['data']
            print("Found nested data, extracting character data from 'data' key")
        else:
            character_data = raw_data
            print("Using direct character data")
        
        print("Parsed character data:", character_data)
        
        # Validar campos requeridos con logging detallado
        required_fields = ['name', 'gender', 'archetype']
        missing_fields = []
        
        for field in required_fields:
            value = character_data.get(field)
            print(f"Field '{field}': {value} (type: {type(value)})")
            if not value or (isinstance(value, str) and not value.strip()):
                missing_fields.append(field)
        
        if missing_fields:
            error_msg = f"Campos requeridos faltantes: {', '.join(missing_fields)}"
            print("ERROR:", error_msg)
            return Response(
                {"error": error_msg, "received_data": character_data},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear el personaje directamente con mejor manejo de campos
        try:
            # Determinar qu+Æ usuario usar para el personaje
            from ..models import User
            
            # Estrategia: usar el usuario autenticado si existe, sino usar usuario de prueba
            if hasattr(request, 'user') and request.user and request.user.is_authenticated:
                # Si hay un usuario autenticado, usar ese
                character_user = request.user
                print(f"Using authenticated user: {character_user.username}")
            else:
                # Si no hay usuario autenticado, usar el primer usuario disponible o crear uno de prueba
                character_user = User.objects.first()
                if not character_user:
                    # Solo crear usuario de prueba si no existe ninguno
                    import uuid
                    unique_id = str(uuid.uuid4())[:8]
                    character_user = User(
                        username=f"test_user_{unique_id}",
                        email=f"test_{unique_id}@example.com",
                        password="test_password"
                    )
                    character_user.save()
                    print(f"Created new test user: {character_user.username}")
                else:
                    print(f"Using existing user for unauthenticated request: {character_user.username}")
            
            character = Character(
                user=character_user,  # Usar el usuario determinado (autenticado o de prueba)
                name=character_data.get('name', '').strip(),
                age=int(character_data.get('age', 0)) if character_data.get('age') else 0,
                gender=character_data.get('gender', '').strip(),
                archetype=character_data.get('archetype', '').strip(),
                background=character_data.get('background', '').strip(),
                personality_traits=character_data.get('personality_traits', []) if character_data.get('personality_traits') else [],
                physical_traits=character_data.get('physical_traits', []) if character_data.get('physical_traits') else [],
                weaknesses=character_data.get('weaknesses', []) if character_data.get('weaknesses') else [],
                special_abilities=character_data.get('special_abilities', '').strip(),
                goals=character_data.get('goals', '').strip(),
                aiFilter=character_data.get('aiFilter', {}) if character_data.get('aiFilter') else {}
            )
            
            print("Character object created, attempting to save...")
            character.save()
            print("Character saved successfully with ID:", character.id)
            
            # Serializar la respuesta
            serializer = CharacterSerializer(character)
            response_data = serializer.data
            print("Response data:", response_data)
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except ValueError as ve:
            error_msg = f"Error de valor en los datos: {str(ve)}"
            print("VALUE ERROR:", error_msg)
            return Response(
                {"error": error_msg, "details": "Revisa los tipos de datos enviados"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as save_error:
            error_msg = f"Error al guardar en base de datos: {str(save_error)}"
            print("SAVE ERROR:", error_msg)
            import traceback
            traceback.print_exc()
            return Response(
                {"error": error_msg, "details": "Error interno del servidor"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    except Exception as e:
        error_msg = f"Error general al crear personaje: {str(e)}"
        print("GENERAL ERROR:", error_msg)
        import traceback
        traceback.print_exc()
        return Response(
            {"error": error_msg, "details": "Error inesperado en el servidor"},
            status=status.HTTP_400_BAD_REQUEST
        )
