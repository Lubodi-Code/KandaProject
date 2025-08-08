from rest_framework import serializers
from ..models import Character
import logging

logger = logging.getLogger(__name__)


class CharacterSerializer(serializers.Serializer):
    """Serializer for Character model using MongoEngine."""
    
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    age = serializers.IntegerField(required=False, default=0)
    archetype = serializers.CharField(max_length=100, required=True)
    gender = serializers.CharField(max_length=50, required=True)
    physical_traits = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    personality_traits = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    weaknesses = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    background = serializers.CharField(required=False, default="")
    special_abilities = serializers.CharField(required=False, default="")
    goals = serializers.CharField(required=False, default="")
    aiFilter = serializers.DictField(required=False)
    is_default = serializers.BooleanField(required=False, default=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def validate(self, data):
        """Validaci+¦n personalizada con logging detallado."""
        logger.info(f"CharacterSerializer validating data: {data}")
        
        # Verificar tipos de datos para campos cr+¡ticos
        name = data.get('name')
        archetype = data.get('archetype')
        gender = data.get('gender')
        
        logger.info(f"name: {name} (type: {type(name)})")
        logger.info(f"archetype: {archetype} (type: {type(archetype)})")
        logger.info(f"gender: {gender} (type: {type(gender)})")
        
        # Validar que name, archetype y gender sean strings
        if name and not isinstance(name, str):
            raise serializers.ValidationError({
                'name': f'Debe ser una cadena de texto, recibido: {type(name).__name__}'
            })
        
        if archetype and not isinstance(archetype, str):
            raise serializers.ValidationError({
                'archetype': f'Debe ser una cadena de texto, recibido: {type(archetype).__name__}'
            })
        
        if gender and not isinstance(gender, str):
            raise serializers.ValidationError({
                'gender': f'Debe ser una cadena de texto, recibido: {type(gender).__name__}'
            })
        
        return data
    
    def create(self, validated_data):
        """Create and return a new Character instance."""
        # El usuario se asignar+í en la vista
        user = self.context['request'].user
        validated_data['user'] = user
        character = Character(**validated_data)
        character.save()
        return character
    
    def update(self, instance, validated_data):
        """Update and return an existing Character instance."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """Override to properly serialize MongoDB ObjectId and references."""
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        data['user'] = str(instance.user.id) if instance.user else None
        return data
