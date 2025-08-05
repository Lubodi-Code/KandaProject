# Kanda Project - Generador de Personajes con IA

Kanda es una aplicación web que utiliza inteligencia artificial para generar perfiles detallados de personajes ficticios a partir de descripciones básicas proporcionadas por los usuarios.

## Arquitectura del Proyecto

El proyecto sigue una arquitectura de microservicios con las siguientes componentes principales:

- **Frontend**: Aplicación Vue.js que proporciona la interfaz de usuario.
- **Backend**: API REST desarrollada con Django y Django REST Framework.
- **Base de Datos**: MongoDB para almacenamiento de datos.
- **Procesamiento Asíncrono**: Celery para tareas en segundo plano.
- **IA**: Integración con la API de OpenAI para la generación de contenido.

## Estructura del Proyecto

```
KandaProyect/
├── KandaBackEnd/           # Backend Django
│   ├── KandaBackend/       # Configuración principal
│   │   ├── __init__.py
│   │   ├── celery.py       # Configuración de Celery
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── api/                # Aplicación principal
│   │   ├── models.py       # Modelos de datos MongoDB
│   │   ├── serializers.py  # Serializadores REST
│   │   ├── tasks.py        # Tareas asíncronas de Celery
│   │   ├── utils.py        # Utilidades
│   │   ├── views.py        # Vistas tradicionales
│   │   ├── api_views.py    # Vistas API de autenticación
│   │   ├── character_views.py # Vistas API de personajes
│   │   └── monitoring_views.py # Vistas de monitoreo
│   └── manage.py
├── KandaFrontEnd/          # Frontend Vue.js
└── requirements.txt        # Dependencias del proyecto
```

## Flujo de Trabajo

1. El usuario se registra y activa su cuenta mediante correo electrónico.
2. El usuario crea un nuevo personaje proporcionando un nombre y una descripción básica.
3. El backend envía la solicitud a una tarea asíncrona de Celery.
4. Celery procesa la solicitud utilizando la API de OpenAI para generar el perfil detallado.
5. El resultado se almacena en la base de datos MongoDB.
6. El usuario puede ver, editar, exportar o eliminar sus personajes.

## Modelos de Datos

### User
- Información básica del usuario (nombre, correo, contraseña)
- Preferencias y configuración
- Límites de uso

### CharacterProfile
- Información básica (nombre, descripción)
- Datos generados por IA (personalidad, historia, apariencia, etc.)
- Estado de procesamiento
- Historial de versiones

## API Endpoints

### Autenticación
- `/api-login/` - Iniciar sesión
- `/api-register/` - Registrar nuevo usuario
- `/api-activate/<uidb64>/<token>/` - Activar cuenta

### Gestión de Personajes
- `/api/characters/` - Listar personajes
- `/api/characters/create/` - Crear personaje
- `/api/characters/<id>/` - Ver personaje
- `/api/characters/<id>/update/` - Actualizar personaje
- `/api/characters/<id>/delete/` - Eliminar personaje
- `/api/characters/<id>/status/` - Ver estado de procesamiento
- `/api/characters/<id>/retry/` - Reintentar procesamiento
- `/api/characters/<id>/export/` - Exportar personaje

### Monitoreo
- `/api/statistics/user/` - Estadísticas del usuario
- `/api/statistics/admin/` - Estadísticas globales (admin)
- `/api/system/health/` - Estado del sistema (admin)

## Configuración y Despliegue

### Requisitos
- Python 3.8+
- Node.js 16+
- MongoDB
- Redis

### Instalación

1. Clonar el repositorio:
   ```
   git clone https://github.com/tu-usuario/KandaProyect.git
   cd KandaProyect
   ```

2. Configurar el entorno virtual y instalar dependencias:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configurar variables de entorno:
   Crear un archivo `.env` en la carpeta `KandaBackEnd/KandaBackend/` con:
   ```
   MONGODB_PASSWORD=tu_contraseña
   SECRET_KEY=tu_clave_secreta
   EMAIL_HOST_USER=tu_email
   EMAIL_HOST_PASSWORD=tu_contraseña_email
   OPENAI_API_KEY=tu_clave_api_openai
   OPENAI_MODEL=gpt-3.5-turbo
   ```

4. Iniciar el servidor de desarrollo:
   ```
   cd KandaBackEnd
   python manage.py runserver
   ```

5. En otra terminal, iniciar Celery:
   ```
   cd KandaBackEnd
   celery -A KandaBackend worker --loglevel=info
   ```

6. Configurar y iniciar el frontend:
   ```
   cd KandaFrontEnd
   npm install
   npm run dev
   ```

## Licencia

Este proyecto está licenciado bajo [MIT License](LICENSE).