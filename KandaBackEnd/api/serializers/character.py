from rest_framework import serializers
from ..models import Character


class CharacterSerializer(serializers.ModelSerializer):
    """Serializer for Character model."""

    class Meta:
        model = Character
        fields = [
            "id",
            "user",
            "name",
            "archetype",
            "gender",
            "physical_traits",
            "personality_traits",
            "background",
            "aiFilter",
            "is_default",
        ]
        read_only_fields = ["id", "user", "aiFilter"]
