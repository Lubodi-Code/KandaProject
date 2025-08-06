from rest_framework import serializers
from .models import User, CharacterProfile, ProcessingStatus

class ProcessingStatusSerializer(serializers.Serializer):
    """
    Serializador para el estado de procesamiento de un personaje.
    """
    status = serializers.ChoiceField(
        choices=['pending', 'processing', 'completed', 'failed'],
        default='pending'
    )
    started_at = serializers.DateTimeField(allow_null=True, required=False)
    completed_at = serializers.DateTimeField(allow_null=True, required=False)
    error_message = serializers.CharField(allow_blank=True, required=False)
    attempts = serializers.IntegerField(default=0)
    last_attempt = serializers.DateTimeField(allow_null=True, required=False)


class CharacterProfileSerializer(serializers.Serializer):
    """
    Serializador para los perfiles de personajes.
    """
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True, max_length=100)
    description = serializers.CharField(required=True)
    user = serializers.CharField(read_only=True)  # ID del usuario
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    # Campos generados por la IA
    personality = serializers.DictField(required=False, default=dict)
    background = serializers.DictField(required=False, default=dict)
    appearance = serializers.DictField(required=False, default=dict)
    relationships = serializers.ListField(child=serializers.DictField(), required=False, default=list)
    abilities = serializers.ListField(child=serializers.DictField(), required=False, default=list)
    
    # Estado del procesamiento
    processing_status = ProcessingStatusSerializer(required=False)
    
    # Configuración y metadatos
    is_public = serializers.BooleanField(default=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    version_number = serializers.IntegerField(read_only=True)
    
    def create(self, validated_data):
        """
        Crea un nuevo perfil de personaje.
        """
        user = self.context['request'].user
        
        # Crear perfil
        character = CharacterProfile(
            name=validated_data['name'],
            description=validated_data['description'],
            user=user,
            tags=validated_data.get('tags', []),
            is_public=validated_data.get('is_public', False)
        )
        character.save()
        
        return character
    
    def update(self, instance, validated_data):
        """
        Actualiza un perfil de personaje existente.
        """
        # Actualizar campos básicos
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.is_public = validated_data.get('is_public', instance.is_public)
        
        # Guardar cambios
        instance.save()
        
        return instance


class UserSerializer(serializers.Serializer):
    """
    Serializador para usuarios.
    """
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    max_characters = serializers.IntegerField(read_only=True)
    
    def create(self, validated_data):
        """
        Crea un nuevo usuario.
        """
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        
        return user
    
    def update(self, instance, validated_data):
        """
        Actualiza un usuario existente.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        
        instance.save()
        
        return instance


class CharacterListSerializer(serializers.Serializer):
    """
    Serializador simplificado para listar personajes.
    """
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    processing_status = serializers.CharField(source='processing_status.status', read_only=True)
    is_public = serializers.BooleanField(read_only=True)
    tags = serializers.ListField(child=serializers.CharField(), read_only=True)
    version_number = serializers.IntegerField(read_only=True)