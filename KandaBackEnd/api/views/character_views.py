from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Character
from ..serializers.character import CharacterSerializer
from ..utils.character_ai import generate_ai_filter


class CharacterViewSet(viewsets.ModelViewSet):
    """API endpoint for CRUD operations on characters."""

    serializer_class = CharacterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Character.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        character = serializer.save(user=self.request.user)
        ai_data = generate_ai_filter(character)
        if ai_data:
            character.aiFilter.update(ai_data)
            character.save()

    def perform_update(self, serializer):
        character = serializer.save()
        ai_data = generate_ai_filter(character)
        if ai_data:
            character.aiFilter.update(ai_data)
            character.save()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_default_character(request):
    """Create a default character for the authenticated user."""
    character = Character.create_default(user=request.user)
    ai_data = generate_ai_filter(character)
    if ai_data:
        character.aiFilter.update(ai_data)
        character.save()
    serializer = CharacterSerializer(character)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
