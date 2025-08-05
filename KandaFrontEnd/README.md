# Kanda Frontend

Frontend para la aplicación Kanda, desarrollado con Vue 3 + Vite y Tailwind CSS.

## Configuración del proyecto

### Requisitos previos

- Node.js (versión 16 o superior)
- npm o yarn

### Instalación

1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd KandaFrontEnd
```

2. Instalar dependencias

```bash
npm install
# o
yarn install
```

3. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` para configurar la URL de la API y otras variables de entorno necesarias.

### Desarrollo

Para iniciar el servidor de desarrollo:

```bash
npm run dev
# o
yarn dev
```

El servidor de desarrollo estará disponible en `http://localhost:5173`.

### Compilación para producción

```bash
npm run build
# o
yarn build
```

## Estructura del proyecto

```
src/
├── api/                # Servicios de API y configuración
│   ├── apiClient.js    # Cliente Axios configurado
│   └── auth.js         # Servicios de autenticación
├── assets/             # Recursos estáticos (CSS, imágenes, etc.)
├── components/         # Componentes Vue reutilizables
├── router/             # Configuración de Vue Router
├── stores/             # Stores de Pinia
└── views/              # Vistas/páginas de la aplicación
    ├── LoginView.vue           # Página de inicio de sesión
    ├── RegisterView.vue        # Página de registro
    ├── ActivationEmailView.vue # Página de verificación de email
    ├── ActivationSuccessView.vue # Página de activación exitosa
    ├── ActivationInvalidView.vue # Página de token inválido
    ├── ResendActivationView.vue  # Página para reenviar email
    ├── DashboardView.vue       # Dashboard (protegido)
    └── NotFoundView.vue        # Página 404
```

## Flujo de autenticación

1. **Registro**: El usuario se registra proporcionando su email, contraseña y datos personales.
2. **Verificación de email**: Se envía un correo de activación al usuario.
3. **Activación de cuenta**: El usuario hace clic en el enlace de activación en su correo.
4. **Inicio de sesión**: Una vez activada la cuenta, el usuario puede iniciar sesión.
5. **Acceso al dashboard**: Después de iniciar sesión, el usuario es redirigido al dashboard.

## Tecnologías utilizadas

- **Vue 3**: Framework progresivo para construir interfaces de usuario.
- **Vite**: Herramienta de compilación rápida para desarrollo moderno.
- **Vue Router**: Enrutador oficial para Vue.js.
- **Pinia**: Biblioteca de gestión de estado para Vue.
- **Axios**: Cliente HTTP basado en promesas para el navegador y Node.js.
- **Tailwind CSS**: Framework CSS de utilidades de primera clase.

## Integración con el backend

Este frontend está diseñado para trabajar con el backend de Django REST Framework ubicado en el directorio `KandaBackEnd`. Asegúrate de que el backend esté en funcionamiento antes de iniciar el frontend.

## Pruebas locales

Para probar el flujo completo de la aplicación:

1. Inicia el servidor de Django:

```bash
cd ../KandaBackEnd
python manage.py runserver
```

2. Inicia el servidor de desarrollo de Vue:

```bash
cd ../KandaFrontEnd
npm run dev
```

3. Abre tu navegador en `http://localhost:5173`
4. Sigue el flujo: Registro → Verificación de correo → Activación → Inicio de sesión → Dashboard
