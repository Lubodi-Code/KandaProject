from rest_framework import serializers
from ..models import Universe, Room, Story, Chapter, PlayerAction, RoomParticipant
import logging

logger = logging.getLogger(__name__)


class UniverseSerializer(serializers.Serializer):
    """Serializer for Universe model."""
    
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=200, required=True)
    description = serializers.CharField(required=True)
    context = serializers.CharField(required=True)
    rules = serializers.CharField(required=False, default="")
    cover_image = serializers.CharField(required=False, default="")
    background_image = serializers.CharField(required=False, default="")
    
    # Configuraciones espec+¡ficas
    time_period = serializers.CharField(required=False, default="")
    location = serializers.CharField(required=False, default="")
    technology_level = serializers.CharField(required=False, default="")
    magic_allowed = serializers.BooleanField(required=False, default=False)
    supernatural_elements = serializers.BooleanField(required=False, default=False)
    
    # Control de acceso
    is_public = serializers.BooleanField(required=False, default=True)
    created_by = serializers.CharField(read_only=True)
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """Create and return a new Universe instance."""
        user = self.context['request'].user
        validated_data['created_by'] = user
        universe = Universe(**validated_data)
        universe.save()
        return universe
    
    def update(self, instance, validated_data):
        """Update and return an existing Universe instance."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """Override to properly serialize MongoDB ObjectId and references."""
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        data['created_by'] = str(instance.created_by.id) if instance.created_by else None
        return data


class RoomSerializer(serializers.Serializer):
    """Serializer for Room model."""
    
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=200, required=True)
    description = serializers.CharField(required=False, default="")
    universe = serializers.CharField(required=True)  # Universe ID
    
    # Control de acceso
    is_public = serializers.BooleanField(required=False, default=True)
    access_code = serializers.CharField(read_only=True)
    max_players = serializers.IntegerField(required=False, default=6)
    
    # Administraci+¦n
    admin = serializers.CharField(read_only=True)
    players = serializers.ListField(child=serializers.CharField(), read_only=True)
    player_count = serializers.SerializerMethodField()
    
    # Estado del juego
    status = serializers.CharField(read_only=True)
    
    # Configuraci+¦n del juego
    total_chapters = serializers.IntegerField(required=False, default=5)
    discussion_time = serializers.IntegerField(required=False, default=300)
    allow_discussion = serializers.BooleanField(required=False, default=True)
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    # Campos adicionales para la respuesta
    universe_name = serializers.SerializerMethodField()
    admin_username = serializers.SerializerMethodField()
    
    def get_player_count(self, obj):
        """Return the number of players in the room."""
        return len(obj.players) if obj.players else 0
    
    def get_universe_name(self, obj):
        """Return the universe name."""
        return obj.universe.name if obj.universe else ""
    
    def get_admin_username(self, obj):
        """Return the admin username."""
        return obj.admin.username if obj.admin else ""
    
    def create(self, validated_data):
        """Create and return a new Room instance."""
        user = self.context['request'].user
        
        # Obtener el universo
        from bson import ObjectId
        universe_id = validated_data.pop('universe')
        universe = Universe.objects.get(id=ObjectId(universe_id))
        
        # Crear la sala
        room = Room(
            admin=user,
            universe=universe,
            **validated_data
        )
        room.save()
        return room
    
    def update(self, instance, validated_data):
        """Update and return an existing Room instance."""
        # Si se est+í actualizando el universo
        if 'universe' in validated_data:
            from bson import ObjectId
            universe_id = validated_data.pop('universe')
            instance.universe = Universe.objects.get(id=ObjectId(universe_id))
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """Override to properly serialize MongoDB ObjectId and references."""
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        data['universe'] = str(instance.universe.id) if instance.universe else None
        data['admin'] = str(instance.admin.id) if instance.admin else None
        data['players'] = [str(player.id) for player in instance.players] if instance.players else []
        return data


class RoomParticipantSerializer(serializers.Serializer):
    """Serializer for RoomParticipant model."""
    
    id = serializers.CharField(read_only=True)
    room = serializers.CharField(required=True)  # Room ID
    user = serializers.CharField(read_only=True)
    characters = serializers.ListField(child=serializers.CharField(), required=True)  # Character IDs
    joined_at = serializers.DateTimeField(read_only=True)
    is_ready = serializers.BooleanField(required=False, default=False)
    
    # Campos adicionales para la respuesta
    user_username = serializers.SerializerMethodField()
    character_names = serializers.SerializerMethodField()
    
    def get_user_username(self, obj):
        """Return the username."""
        return obj.user.username if obj.user else ""
    
    def get_character_names(self, obj):
        """Return the character names."""
        return [char.name for char in obj.characters] if obj.characters else []
    
    def create(self, validated_data):
        """Create and return a new RoomParticipant instance."""
        user = self.context['request'].user
        
        # Obtener la sala
        from bson import ObjectId
        room_id = validated_data.pop('room')
        room = Room.objects.get(id=ObjectId(room_id))
        
        # Obtener los personajes
        character_ids = validated_data.pop('characters')
        from ..models import Character
        characters = [Character.objects.get(id=ObjectId(char_id)) for char_id in character_ids]
        
        # Crear el participante
        participant = RoomParticipant(
            room=room,
            user=user,
            characters=characters,
            **validated_data
        )
        participant.save()
        
        # A+¦adir el usuario a la sala
        room.add_player(user)
        
        return participant
    
    def to_representation(self, instance):
        """Override to properly serialize MongoDB ObjectId and references."""
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        data['room'] = str(instance.room.id) if instance.room else None
        data['user'] = str(instance.user.id) if instance.user else None
        data['characters'] = [str(char.id) for char in instance.characters] if instance.characters else []
        return data


class StorySerializer(serializers.Serializer):
    """Serializer for Story model."""
    
    id = serializers.CharField(read_only=True)
    room = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=300, required=False)
    total_chapters = serializers.IntegerField(required=True)
    current_chapter = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    started_at = serializers.DateTimeField(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)
    
    # Campos adicionales
    room_name = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    def get_room_name(self, obj):
        """Return the room name."""
        return obj.room.name if obj.room else ""
    
    def get_progress_percentage(self, obj):
        """Return the progress percentage."""
        if obj.total_chapters > 0:
            return round((obj.current_chapter / obj.total_chapters) * 100, 2)
        return 0
    
    def to_representation(self, instance):
        """Override to properly serialize MongoDB ObjectId and references."""
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        data['room'] = str(instance.room.id) if instance.room else None
        return data


class ChapterSerializer(serializers.Serializer):
    """Serializer for Chapter model."""
    
    id = serializers.CharField(read_only=True)
    story = serializers.CharField(read_only=True)
    chapter_number = serializers.IntegerField(required=True)
    content = serializers.CharField(required=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)
    
    # Campos adicionales
    word_count = serializers.SerializerMethodField()
    
    def get_word_count(self, obj):
        """Return the word count of the content."""
        return len(obj.content.split()) if obj.content else 0
    
    def to_representation(self, instance):
        """Override to properly serialize MongoDB ObjectId and references."""
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        data['story'] = str(instance.story.id) if instance.story else None
        return data


class PlayerActionSerializer(serializers.Serializer):
    """Serializer for PlayerAction model."""
    
    id = serializers.CharField(read_only=True)
    chapter = serializers.CharField(required=True)  # Chapter ID
    user = serializers.CharField(read_only=True)
    character = serializers.CharField(required=True)  # Character ID
    action_text = serializers.CharField(required=True)
    submitted_at = serializers.DateTimeField(read_only=True)
    
    # Campos adicionales
    user_username = serializers.SerializerMethodField()
    character_name = serializers.SerializerMethodField()
    
    def get_user_username(self, obj):
        """Return the username."""
        return obj.user.username if obj.user else ""
    
    def get_character_name(self, obj):
        """Return the character name."""
        return obj.character.name if obj.character else ""
    
    def create(self, validated_data):
        """Create and return a new PlayerAction instance."""
        user = self.context['request'].user
        
        # Obtener el cap+¡tulo y personaje
        from bson import ObjectId
        chapter_id = validated_data.pop('chapter')
        character_id = validated_data.pop('character')
        
        chapter = Chapter.objects.get(id=ObjectId(chapter_id))
        from ..models import Character
        character = Character.objects.get(id=ObjectId(character_id))
        
        # Crear la acci+¦n
        action = PlayerAction(
            chapter=chapter,
            user=user,
            character=character,
            **validated_data
        )
        action.save()
        return action
    
    def to_representation(self, instance):
        """Override to properly serialize MongoDB ObjectId and references."""
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        data['chapter'] = str(instance.chapter.id) if instance.chapter else None
        data['user'] = str(instance.user.id) if instance.user else None
        data['character'] = str(instance.character.id) if instance.character else None
        return data
