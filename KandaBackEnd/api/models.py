from mongoengine import Document, StringField, EmailField, BooleanField, DateTimeField, \
    ReferenceField, ListField, DictField, IntField, EmbeddedDocument, EmbeddedDocumentField, \
    EmbeddedDocumentListField, ObjectIdField
from django.contrib.auth.hashers import make_password, check_password
import datetime
from bson import ObjectId

# Create your models here.
class TestModel(Document):
    name = StringField(max_length=100, required=True)

    class Meta:
        verbose_name = 'Test Model'
        verbose_name_plural = 'Test Models'

    def __str__(self):
        return self.name


class ProcessingStatus(EmbeddedDocument):
    """Estado del procesamiento de un personaje por la IA."""
    status = StringField(choices=['pending', 'processing', 'completed', 'failed'], default='pending')
    started_at = DateTimeField()
    completed_at = DateTimeField()
    error_message = StringField()
    attempts = IntField(default=0)
    last_attempt = DateTimeField()


class CharacterProfile(Document):
    """Modelo para los perfiles de personajes generados por IA."""
    name = StringField(required=True)
    description = StringField(required=True)  # Descripción inicial proporcionada por el usuario
    user = ReferenceField('User', required=True)  # Referencia al usuario que creó el personaje
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    
    # Campos generados por la IA
    personality = DictField()  # Rasgos de personalidad, valores, motivaciones
    background = DictField()  # Historia, origen, eventos importantes
    appearance = DictField()  # Descripción física
    relationships = ListField(DictField())  # Relaciones con otros personajes
    abilities = ListField(DictField())  # Habilidades, poderes, talentos
    
    # Estado del procesamiento
    processing_status = EmbeddedDocumentField(ProcessingStatus, default=ProcessingStatus)
    
    # Versiones del perfil
    versions = ListField(DictField())  # Historial de versiones anteriores
    version_number = IntField(default=1)  # Número de versión actual
    
    # Configuración y metadatos
    is_public = BooleanField(default=False)  # Si el perfil es público o privado
    tags = ListField(StringField())  # Etiquetas para categorizar el personaje
    
    meta = {
        'collection': 'character_profiles',
        'indexes': [
            'name',
            'user',
            'created_at',
            'tags',
            {'fields': ['user', 'name'], 'unique': True}
        ]
    }
    
    def __str__(self):
        return f"{self.name} (by {self.user.username})"
    
    def save(self, *args, **kwargs):
        """Actualiza el timestamp de actualización antes de guardar."""
        self.updated_at = datetime.datetime.now()
        return super(CharacterProfile, self).save(*args, **kwargs)
    
    def to_dict(self):
        """Convierte el perfil a un diccionario para exportación."""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'personality': self.personality,
            'background': self.background,
            'appearance': self.appearance,
            'relationships': self.relationships,
            'abilities': self.abilities,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'version': self.version_number
        }


class User(Document):
    username = StringField(max_length=150, required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    is_active = BooleanField(default=False)  # Usuario inactivo hasta confirmar email
    is_staff = BooleanField(default=False)  # No es administrador por defecto
    date_joined = DateTimeField(default=datetime.datetime.now)
    last_login = DateTimeField(default=datetime.datetime.now)
    
    # Campos adicionales para la gestión de personajes
    max_characters = IntField(default=10)  # Límite de personajes que puede crear
    preferences = DictField()  # Preferencias del usuario (tema, notificaciones, etc.)
    
    meta = {
        'collection': 'users',
        'indexes': [
            {'fields': ['username'], 'unique': True},
            {'fields': ['email'], 'unique': True}
        ]
    }
    
    def __str__(self):
        return self.username
    
    def set_password(self, raw_password):
        """Establece la contraseña del usuario con hash seguro."""
        self.password = make_password(raw_password)
        self.save()
    
    def check_password(self, raw_password):
        """Verifica si la contraseña proporcionada coincide con la almacenada."""
        return check_password(raw_password, self.password)
    
    def save(self, *args, **kwargs):
        """Sobrescribe el método save para asegurar que la contraseña tenga hash."""
        # Si la contraseña no tiene hash (no comienza con algoritmos conocidos)
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        return super(User, self).save(*args, **kwargs)
    
    def get_characters(self):
        """Obtiene todos los personajes creados por el usuario."""
        return CharacterProfile.objects(user=self)
        return super(User, self).save(*args, **kwargs)