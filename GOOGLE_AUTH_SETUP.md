# Configuraci+�n de Google Sign-In

## Pasos para configurar la autenticaci+�n con Google

### 1. Obtener Google Client ID

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google Identity
4. Ve a "Credenciales" > "Crear credenciales" > "ID de cliente OAuth 2.0"
5. Configura los or+�genes autorizados:
   - `http://localhost:5173` (para desarrollo)
   - `http://localhost:5174` (puerto alternativo)
   - `http://127.0.0.1:5173`
   - `http://127.0.0.1:5174`

### 2. Configurar Backend

Agrega tu Google Client ID al archivo `.env` del backend:

```env
GOOGLE_CLIENT_ID=tu_google_client_id.apps.googleusercontent.com
```

### 3. Configurar Frontend

Agrega tu Google Client ID al archivo `.env` del frontend:

```env
VITE_GOOGLE_CLIENT_ID=tu_google_client_id.apps.googleusercontent.com
```

### 4. Funcionalidades Implementadas

#### Persistencia de Sesi+�n
- El token se guarda en localStorage
- Se verifica autom+�ticamente al recargar la p+�gina
- Redirecci+�n autom+�tica al dashboard si el usuario ya est+� logueado

#### Login con Google
- Bot+�n "Continuar con Google" en la p+�gina de login
- Verificaci+�n del token de Google en el backend
- Creaci+�n autom+�tica de usuario si no existe
- Mismo sistema de tokens que el login tradicional

#### Guards de Rutas Mejorados
- Verificaci+�n tanto local como en servidor
- Limpieza autom+�tica de tokens inv+�lidos
- Redirecci+�n inteligente seg+�n el estado de autenticaci+�n

### 5. Endpoints del Backend

- `POST /api/api-login/` - Login tradicional
- `POST /api/google-login/` - Login con Google
- `GET /api/test-auth/` - Verificar estado de autenticaci+�n

### 6. Flujo de Autenticaci+�n

1. **Login Tradicional**: Email + contrase+�a ��� Token ��� Dashboard
2. **Login con Google**: Click bot+�n ��� Google One Tap ��� Token ��� Dashboard
3. **Recarga de p+�gina**: Verificar token local ��� Verificar en servidor ��� Dashboard o Login

### 7. Manejo de Errores

- Tokens expirados se limpian autom+�ticamente
- Errores de red se manejan graciosamente
- Mensajes de error espec+�ficos para diferentes casos

### 8. Seguridad

- Tokens con expiraci+�n de 30 d+�as
- Verificaci+�n del token de Google en el backend
- Validaci+�n de email verificado en Google
- Limpieza autom+�tica de tokens inv+�lidos
