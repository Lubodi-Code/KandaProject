import axios from 'axios';
import tokenManager from '../utils/tokenManager';

// Crear una instancia de Axios con la configuración base
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 10000 // 10 segundos de timeout por defecto
});

// Interceptor para añadir el token de autenticación a las solicitudes
apiClient.interceptors.request.use(
  config => {
    const token = tokenManager.getToken();
    if (token) {
      config.headers['Authorization'] = `Token ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores de respuesta
apiClient.interceptors.response.use(
  response => response,
  error => {
    // Manejar errores específicos
    if (error.response) {
      const status = error.response.status;
      const url = error.config?.url;
      
      switch (status) {
        case 401:
          // Solo limpiar token y redirigir si NO es el endpoint de login
          if (!url?.includes('/api-login/')) {
            console.warn('Token expirado o inválido, limpiando sesión');
            tokenManager.clearToken();
            
            // Redirigir a login solo si no estamos ya en login
            if (window.location.pathname !== '/login') {
              window.location.href = '/login';
            }
          }
          // Para el endpoint de login, dejar que el componente maneje el error
          break;
          
        case 403:
          console.warn('Acceso denegado');
          break;
          
        case 404:
          console.warn('Recurso no encontrado:', url);
          break;
          
        case 429:
          console.warn('Demasiadas solicitudes, limitando tasa');
          break;
          
        case 500:
          console.error('Error interno del servidor');
          break;
          
        default:
          console.error('Error HTTP:', status, error.response.data);
      }
    } else if (error.request) {
      console.error('Error de red:', error.message);
    } else {
      console.error('Error de configuración:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;