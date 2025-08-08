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
    description = StringField(required=True)  # Descripci√≥n inicial proporcionada por el usuario
    user = ReferenceField('User', required=True)  # Referencia al usuario que cre√≥ el personaje
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    
    # Campos generados por la IA
    personality = DictField()  # Rasgos de personalidad, valores, motivaciones
    background = DictField()  # Historia, origen, eventos importantes
    appearance = DictField()  # Descripci√≥n f√≠sica
    relationships = ListField(DictField())  # Relaciones con otros personajes
    abilities = ListField(DictField())  # Habilidades, poderes, talentos
    
    # Estado del procesamiento
    processing_status = EmbeddedDocumentField(ProcessingStatus, default=ProcessingStatus)
    
    # Versiones del perfil
    versions = ListField(DictField())  # Historial de versiones anteriores
    version_number = IntField(default=1)  # N√∫mero de versi√≥n actual
    
    # Configuraci√≥n y metadatos
    is_public = BooleanField(default=False)  # Si el perfil es p√∫blico o privado
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
        """Actualiza el timestamp de actualizaci√≥n antes de guardar."""
        self.updated_at = datetime.datetime.now()
        return super(CharacterProfile, self).save(*args, **kwargs)
    
    def to_dict(self):
        """Convierte el perfil a un diccionario para exportaci√≥n."""
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
    
    # Campos adicionales para la gesti√≥n de personajes
    max_characters = IntField(default=10)  # L√≠mite de personajes que puede crear
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
        """Establece la contrase√±a del usuario con hash seguro."""
        self.password = make_password(raw_password)
        self.save()
    
    def check_password(self, raw_password):
        """Verifica si la contrase√±a proporcionada coincide con la almacenada."""
        return check_password(raw_password, self.password)
    
    def save(self, *args, **kwargs):
        """Sobrescribe el m√©todo save para asegurar que la contrase√±a tenga hash."""
        # Si la contrase√±a no tiene hash (no comienza con algoritmos conocidos)
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        return super(User, self).save(*args, **kwargs)
    
    def get_characters(self):
        """Obtiene todos los personajes creados por el usuario."""
        return CharacterProfile.objects(user=self)


class Character(Document):
    """Character linked to a user with an AI filter."""
    
    user = ReferenceField('User', required=True)
    
    # Core attributes
    name = StringField(max_length=100, required=True)
    age = IntField(default=0)
    archetype = StringField(max_length=100, required=True)
    gender = StringField(max_length=50, required=True)
    
    # Descriptive trait collections
    physical_traits = ListField(StringField(), default=list)
    personality_traits = ListField(StringField(), default=list)
    weaknesses = ListField(StringField(), default=list)
    background = StringField(default="")
    
    # New fields for special abilities and motivations
    special_abilities = StringField(default="")
    goals = StringField(default="")  # Motivations/Goals
    
    # AI balancing data
    aiFilter = DictField(default=lambda: {"powerLevel": 5, "strengths": [], "flaws": [], "accepted": False})
    is_default = BooleanField(default=False)
    
    # Timestamps
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    
    meta = {
        'collection': 'characters',
        'indexes': [
            'name',
            'user',
            'archetype',
            'created_at'
        ]
    }
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Actualiza el timestamp de actualizaci+¶n antes de guardar."""
        self.updated_at = datetime.datetime.now()
        return super(Character, self).save(*args, **kwargs)
    
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
            weaknesses=["inexperienced"],
            background="",
            is_default=True,
        )


# Modelo para Universos/Series
class Universe(Document):
    """Universo o serie donde se desarrollan las historias."""
    
    name = StringField(max_length=200, required=True)
    description = StringField(required=True)  # Descripci+¶n del universo
    context = StringField(required=True)  # Contexto temporal/espacial
    rules = StringField()  # Reglas espec+°ficas del universo
    cover_image = StringField()  # URL de la portada
    background_image = StringField()  # URL de imagen de fondo
    
    # Configuraciones espec+°ficas
    time_period = StringField()  # +Îpoca temporal
    location = StringField()  # Ubicaci+¶n geogr+Ìfica/espacial
    technology_level = StringField()  # Nivel tecnol+¶gico
    magic_allowed = BooleanField(default=False)  # Si se permite magia
    supernatural_elements = BooleanField(default=False)  # Elementos sobrenaturales
    
    # Control de acceso
    is_public = BooleanField(default=True)  # Si es p+¶blico o privado
    created_by = ReferenceField('User', required=False)  # Creador del universo (temporalmente opcional)
    
    # Timestamps
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    
    meta = {
        'collection': 'universes',
        'indexes': [
            'name',
            'created_by',
            'is_public',
            'created_at'
        ]
    }
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Actualiza el timestamp de actualizaci+¶n antes de guardar."""
        self.updated_at = datetime.datetime.now()
        return super(Universe, self).save(*args, **kwargs)


# Modelo para Salas de Juego
class Room(Document):
    """Sala donde los jugadores se re+¶nen para jugar."""
    
    name = StringField(max_length=200, required=True)
    description = StringField()
    universe = ReferenceField(Universe, required=True)  # Universo seleccionado
    
    # Control de acceso
    is_public = BooleanField(default=True)  # Sala p+¶blica o privada
    access_code = StringField()  # C+¶digo para salas privadas
    max_players = IntField(default=6)  # M+Ìximo de jugadores
    
    # Administraci+¶n
    admin = ReferenceField('User', required=True)  # Administrador de la sala
    players = ListField(ReferenceField('User'))  # Lista de jugadores
    
    # Estado del juego
    status = StringField(choices=['waiting', 'playing', 'finished'], default='waiting')
    
    # Configuraci+¶n del juego
    total_chapters = IntField(default=5)  # N+¶mero total de cap+°tulos
    discussion_time = IntField(default=300)  # Tiempo de discusi+¶n en segundos (5 min)
    allow_discussion = BooleanField(default=True)  # Si permite discusi+¶n
    
    # Timestamps
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    
    meta = {
        'collection': 'rooms',
        'indexes': [
            'name',
            'admin',
            'is_public',
            'status',
            'access_code',
            'created_at'
        ]
    }
    
    def __str__(self):
        return f"{self.name} - {self.universe.name}"
    
    def save(self, *args, **kwargs):
        """Actualiza el timestamp y genera c+¶digo de acceso si es privada."""
        self.updated_at = datetime.datetime.now()
        
        # Generar c+¶digo de acceso para salas privadas
        if not self.is_public and not self.access_code:
            import random
            import string
            self.access_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        return super(Room, self).save(*args, **kwargs)
    
    def add_player(self, user):
        """A+¶adir un jugador a la sala."""
        if user not in self.players and len(self.players) < self.max_players:
            self.players.append(user)
            self.save()
            return True
        return False
    
    def remove_player(self, user):
        """Remover un jugador de la sala."""
        if user in self.players:
            self.players.remove(user)
            self.save()
            return True
        return False


# Modelo para Participantes en Salas
class RoomParticipant(Document):
    """Relaci+¶n entre usuario, sala y personajes seleccionados."""
    
    room = ReferenceField(Room, required=True)
    user = ReferenceField('User', required=True)
    characters = ListField(ReferenceField(Character))  # Personajes seleccionados
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_ready = BooleanField(default=False)  # Si est+Ì listo para empezar
    
    meta = {
        'collection': 'room_participants',
        'indexes': [
            ('room', 'user'),  # +Ïndice compuesto
            'room',
            'user'
        ]
    }
    
    def __str__(self):
        return f"{self.user.username} en {self.room.name}"


# Modelo para Historias
class Story(Document):
    """Historia generada por IA en una sala."""
    
    room = ReferenceField(Room, required=True)
    title = StringField(max_length=300)
    
    # Configuraci+¶n
    total_chapters = IntField(required=True)
    current_chapter = IntField(default=0)
    
    # Estado
    status = StringField(choices=['in_progress', 'completed', 'paused'], default='in_progress')
    
    # Timestamps
    started_at = DateTimeField(default=datetime.datetime.now)
    completed_at = DateTimeField()
    
    meta = {
        'collection': 'stories',
        'indexes': [
            'room',
            'status',
            'started_at'
        ]
    }
    
    def __str__(self):
        return f"Historia: {self.title or f'Sala {self.room.name}'}"


# Modelo para Cap+°tulos
class Chapter(Document):
    """Cap+°tulo individual de una historia."""
    
    story = ReferenceField(Story, required=True)
    chapter_number = IntField(required=True)
    content = StringField(required=True)  # Contenido generado por IA
    
    # Estado del cap+°tulo
    status = StringField(choices=['writing', 'discussion', 'completed'], default='writing')
    
    # Timestamps
    created_at = DateTimeField(default=datetime.datetime.now)
    completed_at = DateTimeField()
    
    meta = {
        'collection': 'chapters',
        'indexes': [
            'story',
            'chapter_number',
            'created_at'
        ]
    }
    
    def __str__(self):
        return f"Cap+°tulo {self.chapter_number} - {self.story.title}"


# Modelo para Acciones de Jugadores
class PlayerAction(Document):
    """Acciones propuestas por jugadores durante la discusi+¶n."""
    
    chapter = ReferenceField(Chapter, required=True)
    user = ReferenceField('User', required=True)
    character = ReferenceField(Character, required=True)
    action_text = StringField(required=True)  # Acci+¶n propuesta
    
    # Timestamps
    submitted_at = DateTimeField(default=datetime.datetime.now)
    
    meta = {
        'collection': 'player_actions',
        'indexes': [
            'chapter',
            'user',
            'character',
            'submitted_at'
        ]
    }
    
    def __str__(self):
        return f"{self.user.username} ({self.character.name}): {self.action_text[:50]}..."