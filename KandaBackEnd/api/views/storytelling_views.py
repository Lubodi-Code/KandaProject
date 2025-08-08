from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from bson import ObjectId
import logging
import random
import string
from django.utils import timezone

from ..models import Universe, Room, Story, Chapter, PlayerAction, RoomParticipant, Character, User
from ..serializers.storytelling import (
    UniverseSerializer, RoomSerializer, StorySerializer, 
    ChapterSerializer, PlayerActionSerializer, RoomParticipantSerializer
)
from ..auth.token_authentication import CustomTokenAuthentication

logger = logging.getLogger(__name__)


class UniverseViewSet(viewsets.ViewSet):
    """API endpoint for CRUD operations on universes."""
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication, SessionAuthentication]
    
    def list(self, request):
        """List all public universes or user's own universes."""
        try:
            # Obtener universos p+¦blicos y los del usuario
            universes = Universe.objects.filter(
                __raw__={
                    '$or': [
                        {'is_public': True},
                        {'created_by': ObjectId(str(request.user.id))}
                    ]
                }
            ).order_by('-created_at')
            
            serializer = UniverseSerializer(universes, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error listing universes: {str(e)}")
            return Response(
                {"error": f"Error al obtener universos: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, pk=None):
        """Get a specific universe."""
        try:
            universe = Universe.objects.get(id=ObjectId(pk))
            
            # Verificar que sea p+¦blico o del usuario
            if not universe.is_public and str(universe.created_by.id) != str(request.user.id):
                return Response(
                    {"error": "No tienes acceso a este universo"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = UniverseSerializer(universe, context={'request': request})
            return Response(serializer.data)
        except Universe.DoesNotExist:
            return Response(
                {"error": "Universo no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error al obtener el universo: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def create(self, request):
        """Create a new universe (admin only)."""
        try:
            # Verificar que el usuario sea admin o tenga permisos
            if not request.user.is_staff:
                return Response(
                    {"error": "Solo los administradores pueden crear universos"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = UniverseSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                universe = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating universe: {str(e)}")
            return Response(
                {"error": f"Error al crear el universo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def update(self, request, pk=None):
        """Update a universe (admin or creator only)."""
        try:
            universe = Universe.objects.get(id=ObjectId(pk))
            
            # Verificar permisos
            if not request.user.is_staff and str(universe.created_by.id) != str(request.user.id):
                return Response(
                    {"error": "No tienes permisos para editar este universo"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = UniverseSerializer(universe, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                updated_universe = serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Universe.DoesNotExist:
            return Response(
                {"error": "Universo no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error al actualizar el universo: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, pk=None):
        """Delete a universe (admin or creator only)."""
        try:
            universe = Universe.objects.get(id=ObjectId(pk))
            
            # Verificar permisos
            if not request.user.is_staff and str(universe.created_by.id) != str(request.user.id):
                return Response(
                    {"error": "No tienes permisos para eliminar este universo"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            universe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Universe.DoesNotExist:
            return Response(
                {"error": "Universo no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error al eliminar el universo: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class RoomViewSet(viewsets.ViewSet):
    """API endpoint for CRUD operations on rooms."""
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication, SessionAuthentication]
    
    def list(self, request):
        """List all public rooms."""
        try:
            rooms = Room.objects.filter(is_public=True, status='waiting').order_by('-created_at')
            serializer = RoomSerializer(rooms, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error listing rooms: {str(e)}")
            return Response(
                {"error": f"Error al obtener salas: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def my_rooms(self, request):
        """Get rooms created by the current user."""
        try:
            rooms = Room.objects.filter(admin=request.user).order_by('-created_at')
            serializer = RoomSerializer(rooms, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error getting user rooms: {str(e)}")
            return Response(
                {"error": f"Error al obtener tus salas: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def joined_rooms(self, request):
        """Get rooms where the user is a participant."""
        try:
            # Obtener salas donde el usuario es participante
            participants = RoomParticipant.objects.filter(user=request.user)
            room_ids = [p.room.id for p in participants]
            rooms = Room.objects.filter(id__in=room_ids).order_by('-created_at')
            
            serializer = RoomSerializer(rooms, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error getting joined rooms: {str(e)}")
            return Response(
                {"error": f"Error al obtener salas unidas: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, pk=None):
        """Get a specific room."""
        try:
            room = Room.objects.get(id=ObjectId(pk))
            serializer = RoomSerializer(room, context={'request': request})
            return Response(serializer.data)
        except Room.DoesNotExist:
            return Response(
                {"error": "Sala no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error al obtener la sala: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def create(self, request):
        """Create a new room."""
        try:
            serializer = RoomSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                room = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating room: {str(e)}")
            return Response(
                {"error": f"Error al crear la sala: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a room."""
        try:
            room = Room.objects.get(id=ObjectId(pk))
            
            # Verificar si la sala est+í disponible
            if room.status != 'waiting':
                return Response(
                    {"error": "La sala no est+í disponible para nuevos jugadores"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verificar capacidad
            if len(room.players) >= room.max_players:
                return Response(
                    {"error": "La sala est+í llena"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verificar c+¦digo de acceso para salas privadas
            if not room.is_public:
                provided_code = request.data.get('access_code', '')
                if provided_code != room.access_code:
                    return Response(
                        {"error": "C+¦digo de acceso incorrecto"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # A+¦adir el usuario a la sala
            if room.add_player(request.user):
                serializer = RoomSerializer(room, context={'request': request})
                return Response(serializer.data)
            else:
                return Response(
                    {"error": "No se pudo unir a la sala"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Room.DoesNotExist:
            return Response(
                {"error": "Sala no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error al unirse a la sala: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a room."""
        try:
            room = Room.objects.get(id=ObjectId(pk))
            
            if room.remove_player(request.user):
                # Tambi+®n eliminar el participante
                try:
                    participant = RoomParticipant.objects.get(room=room, user=request.user)
                    participant.delete()
                except RoomParticipant.DoesNotExist:
                    pass
                
                return Response({"message": "Has salido de la sala"})
            else:
                return Response(
                    {"error": "No est+ís en esta sala"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Room.DoesNotExist:
            return Response(
                {"error": "Sala no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error al salir de la sala: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def start_game(self, request, pk=None):
        """Start the game (admin only)."""
        try:
            room = Room.objects.get(id=ObjectId(pk))
            
            # Verificar que sea el admin
            if str(room.admin.id) != str(request.user.id):
                return Response(
                    {"error": "Solo el administrador puede iniciar el juego"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Validaciones de estado
            if room.status == 'playing':
                return Response({"error": "El juego ya est+í en progreso"}, status=status.HTTP_400_BAD_REQUEST)
            if room.status != 'waiting':
                return Response({"error": "La sala no est+í lista para iniciar"}, status=status.HTTP_400_BAD_REQUEST)

            # No iniciar si ya hay una historia activa
            existing_story = Story.objects.filter(room=room, status='in_progress').first()
            if existing_story:
                return Response({"error": "Ya existe una historia activa para esta sala"}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar participantes y que todos est+®n listos y con personajes
            participants = RoomParticipant.objects.filter(room=room)
            if not participants:
                return Response({"error": "Se necesita al menos un participante para empezar"}, status=status.HTTP_400_BAD_REQUEST)

            not_ready = []
            no_characters = []
            for p in participants:
                if not p.is_ready:
                    not_ready.append(p.user.username if hasattr(p.user, 'username') else str(p.user.id))
                if not p.characters:
                    no_characters.append(p.user.username if hasattr(p.user, 'username') else str(p.user.id))

            if not_ready:
                return Response({
                    "error": "Todos los participantes deben estar listos",
                    "details": {"no_listos": not_ready}
                }, status=status.HTTP_400_BAD_REQUEST)

            if no_characters:
                return Response({
                    "error": "Todos los participantes deben tener al menos un personaje asignado",
                    "details": {"sin_personajes": no_characters}
                }, status=status.HTTP_400_BAD_REQUEST)

            # Verificar que haya jugadores
            if len(room.players) == 0:
                return Response({"error": "Se necesita al menos un jugador para empezar"}, status=status.HTTP_400_BAD_REQUEST)

            # Actualizar estado de la sala
            room.status = 'playing'
            room.save()

            # Crear la historia
            story = Story(
                room=room,
                title=f"Historia de {room.name}",
                total_chapters=room.total_chapters
            )
            story.save()

            return Response({
                "message": "Juego iniciado",
                "story_id": str(story.id)
            })
        except Room.DoesNotExist:
            return Response(
                {"error": "Sala no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def submit_action(self, request, pk=None):
        """Submit a player action for the current chapter."""
        try:
            room = Room.objects.get(id=ObjectId(pk))
            # Obtener la historia en curso
            story = Story.objects.filter(room=room, status='in_progress').first()
            if not story:
                return Response({"error": "No hay historia activa"}, status=status.HTTP_400_BAD_REQUEST)

            # Cap+¡tulo objetivo
            chapter_id = request.data.get('chapter')
            if not chapter_id:
                return Response({"error": "chapter es requerido"}, status=status.HTTP_400_BAD_REQUEST)
            chapter = Chapter.objects.get(id=ObjectId(chapter_id))

            # Encontrar el participante y un personaje del usuario
            participant = RoomParticipant.objects.filter(room=room, user=request.user).first()
            if not participant or not participant.characters:
                return Response({"error": "Debes seleccionar personajes antes"}, status=status.HTTP_400_BAD_REQUEST)
            character = participant.characters[0]

            # Crear acci+¦n
            action = PlayerAction(
                chapter=chapter,
                user=request.user,
                character=character,
                action_text=request.data.get('action_text', '').strip()
            )
            if not action.action_text:
                return Response({"error": "action_text es requerido"}, status=status.HTTP_400_BAD_REQUEST)
            action.save()

            serializer = PlayerActionSerializer(action, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Chapter.DoesNotExist:
            return Response({"error": "Cap+¡tulo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Room.DoesNotExist:
            return Response({"error": "Sala no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error submitting action: {str(e)}")
            return Response({"error": f"Error al enviar acci+¦n: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def generate_narrative(self, request, pk=None):
        """Generate or advance narrative for the room's active story by creating the next chapter."""
        try:
            room = Room.objects.get(id=ObjectId(pk))
            story = Story.objects.filter(room=room, status='in_progress').first()
            if not story:
                return Response({"error": "No hay historia activa"}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener universo y participantes para contexto
            universe = room.universe
            participants = RoomParticipant.objects.filter(room=room)
            character_names = []
            for p in participants:
                character_names.extend([c.name for c in p.characters])

            # Preparar n+¦mero de cap+¡tulo siguiente
            next_chapter_num = story.current_chapter + 1
            if next_chapter_num > story.total_chapters:
                story.status = 'completed'
                story.completed_at = timezone.now()
                story.save()
                return Response({"narrative": "La historia ha finalizado."})

            # Recopilar +¦ltimas acciones (si existe cap+¡tulo previo)
            last_actions_text = ''
            try:
                if story.current_chapter > 0:
                    prev = Chapter.objects.get(story=story, chapter_number=story.current_chapter)
                    actions = PlayerAction.objects.filter(chapter=prev).order_by('submitted_at')
                    if actions:
                        last_actions_text = "\n\nAcciones de los jugadores: " + "; ".join([a.action_text for a in actions])
            except Exception:
                pass

            # Generar narrativa b+ísica (placeholder de IA)
            intro = f"Cap+¡tulo {next_chapter_num}: "
            setting = f"En el universo '{universe.name}', {universe.description[:200]}..." if universe and universe.description else ""
            chars = f" Los protagonistas: {', '.join(character_names)}." if character_names else ""
            development = " La historia avanza con giros inesperados y decisiones cruciales." \
                " La atm+¦sfera se intensifica mientras el destino del mundo pende de un hilo."
            narrative = intro + setting + chars + development + last_actions_text

            # Crear cap+¡tulo
            chapter = Chapter(
                story=story,
                chapter_number=next_chapter_num,
                content=narrative,
                status='completed'
            )
            chapter.save()

            # Avanzar historia
            story.current_chapter = next_chapter_num
            story.save()

            return Response({"narrative": narrative, "chapter_id": str(chapter.id)})
        except Room.DoesNotExist:
            return Response({"error": "Sala no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error generating narrative: {str(e)}")
            return Response({"error": f"Error al generar narrativa: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Error al iniciar el juego: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class RoomParticipantViewSet(viewsets.ViewSet):
    """API endpoint for room participants."""
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication, SessionAuthentication]
    
    def create(self, request):
        """Add characters to a room."""
        try:
            serializer = RoomParticipantSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                participant = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error adding participant: {str(e)}")
            return Response(
                {"error": f"Error al a+¦adir participante: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def by_room(self, request):
        """Get participants by room ID."""
        try:
            room_id = request.query_params.get('room_id')
            if not room_id:
                return Response(
                    {"error": "room_id es requerido"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            participants = RoomParticipant.objects.filter(room=ObjectId(room_id))
            serializer = RoomParticipantSerializer(participants, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error getting room participants: {str(e)}")
            return Response(
                {"error": f"Error al obtener participantes: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def partial_update(self, request, pk=None):
        """Update participant readiness (is_ready)."""
        try:
            participant = RoomParticipant.objects.get(id=ObjectId(pk))
            if str(participant.user.id) != str(request.user.id):
                return Response({"error": "No puedes modificar a otros participantes"}, status=status.HTTP_403_FORBIDDEN)

            # Update readiness
            if 'is_ready' in request.data:
                participant.is_ready = bool(request.data['is_ready'])
                participant.save()

            # Update characters selection (only while room is waiting)
            if 'characters' in request.data:
                if participant.room.status != 'waiting':
                    return Response({"error": "No puedes cambiar personajes con el juego en progreso"}, status=status.HTTP_400_BAD_REQUEST)
                chars = request.data.get('characters') or []
                if not isinstance(chars, list) or not chars:
                    return Response({"error": "characters debe ser una lista no vac+¡a"}, status=status.HTTP_400_BAD_REQUEST)
                from ..models import Character as CharacterModel
                new_chars = []
                for cid in chars:
                    try:
                        ch = CharacterModel.objects.get(id=ObjectId(cid))
                        # Optional: ensure character belongs to user
                        if str(ch.user.id) != str(request.user.id):
                            return Response({"error": "Solo puedes asignar tus propios personajes"}, status=status.HTTP_400_BAD_REQUEST)
                        new_chars.append(ch)
                    except Exception:
                        return Response({"error": f"Personaje inv+ílido: {cid}"}, status=status.HTTP_400_BAD_REQUEST)
                participant.characters = new_chars
                participant.save()
            serializer = RoomParticipantSerializer(participant, context={'request': request})
            return Response(serializer.data)
        except RoomParticipant.DoesNotExist:
            return Response({"error": "Participante no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating participant: {str(e)}")
            return Response({"error": f"Error al actualizar participante: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class StoryViewSet(viewsets.ViewSet):
    """Read-only endpoints for stories."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication, SessionAuthentication]

    def list(self, request):
        try:
            room_id = request.query_params.get('room')
            if not room_id:
                return Response({"error": "room es requerido"}, status=status.HTTP_400_BAD_REQUEST)
            story = Story.objects.filter(room=ObjectId(room_id)).order_by('-started_at').first()
            if not story:
                return Response([] if request.query_params.get('as_list') else {}, status=status.HTTP_200_OK)
            serializer = StorySerializer(story, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error listing stories: {str(e)}")
            return Response({"error": f"Error al obtener historias: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            story = Story.objects.get(id=ObjectId(pk))
            serializer = StorySerializer(story, context={'request': request})
            return Response(serializer.data)
        except Story.DoesNotExist:
            return Response({"error": "Historia no encontrada"}, status=status.HTTP_404_NOT_FOUND)


class ChapterViewSet(viewsets.ViewSet):
    """Read-only endpoints for chapters."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication, SessionAuthentication]

    def list(self, request):
        try:
            story_id = request.query_params.get('story')
            if not story_id:
                return Response({"error": "story es requerido"}, status=status.HTTP_400_BAD_REQUEST)
            chapters = Chapter.objects.filter(story=ObjectId(story_id)).order_by('chapter_number')
            serializer = ChapterSerializer(chapters, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error listing chapters: {str(e)}")
            return Response({"error": f"Error al obtener cap+¡tulos: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            chapter = Chapter.objects.get(id=ObjectId(pk))
            serializer = ChapterSerializer(chapter, context={'request': request})
            return Response(serializer.data)
        except Chapter.DoesNotExist:
            return Response({"error": "Cap+¡tulo no encontrado"}, status=status.HTTP_404_NOT_FOUND)


class PlayerActionViewSet(viewsets.ViewSet):
    """Endpoints for player actions."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication, SessionAuthentication]

    def list(self, request):
        try:
            chapter_id = request.query_params.get('chapter')
            if not chapter_id:
                return Response({"error": "chapter es requerido"}, status=status.HTTP_400_BAD_REQUEST)
            from ..models import Chapter as ChapterModel
            chapter = ChapterModel.objects.get(id=ObjectId(chapter_id))
            actions = PlayerAction.objects.filter(chapter=chapter).order_by('submitted_at')
            serializer = PlayerActionSerializer(actions, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error listing actions: {str(e)}")
            return Response({"error": f"Error al obtener acciones: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        try:
            serializer = PlayerActionSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                action = serializer.save()
                return Response(PlayerActionSerializer(action, context={'request': request}).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating action: {str(e)}")
            return Response({"error": f"Error al crear acci+¦n: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomTokenAuthentication, SessionAuthentication])
def join_room_with_code(request):
    """Join a private room using access code."""
    try:
        access_code = request.data.get('access_code', '').strip().upper()
        
        if not access_code:
            return Response(
                {"error": "C+¦digo de acceso requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar la sala por c+¦digo
        try:
            room = Room.objects.get(access_code=access_code, is_public=False)
        except Room.DoesNotExist:
            return Response(
                {"error": "C+¦digo de acceso inv+ílido"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verificar disponibilidad
        if room.status != 'waiting':
            return Response(
                {"error": "La sala no est+í disponible"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(room.players) >= room.max_players:
            return Response(
                {"error": "La sala est+í llena"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # A+¦adir el usuario
        if room.add_player(request.user):
            serializer = RoomSerializer(room, context={'request': request})
            return Response(serializer.data)
        else:
            return Response(
                {"error": "No se pudo unir a la sala"},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        logger.error(f"Error joining room with code: {str(e)}")
        return Response(
            {"error": f"Error al unirse con c+¦digo: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
