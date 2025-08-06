from django.conf import settings
from django.db import models


def default_ai_filter():
    """Default structure for the AI filter field."""
    return {"powerLevel": 5, "strengths": [], "flaws": []}


class Character(models.Model):
    """Character linked to a user with an AI filter."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="characters",
    )

    # Core attributes
    name = models.CharField(max_length=100)
    archetype = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)

    # Descriptive trait collections
    physical_traits = models.JSONField(default=list, blank=True)
    personality_traits = models.JSONField(default=list, blank=True)
    background = models.TextField(blank=True, default="")

    # AI balancing data
    aiFilter = models.JSONField(default=default_ai_filter)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @classmethod
    def create_default(cls, user):
        """Create and return a default character for the given user."""
        return cls.objects.create(
            user=user,
            name="Default Character",
            archetype="Hero",
            gender="Unknown",
            physical_traits=["average build"],
            personality_traits=["brave"],
            background="",
            aiFilter=default_ai_filter(),
            is_default=True,
        )
