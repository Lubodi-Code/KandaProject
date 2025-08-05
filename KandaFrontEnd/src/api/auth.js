import apiClient from './apiClient';
import tokenManager from '../utils/tokenManager';

/**
 * Servicio de autenticación para interactuar con la API
 */
export const authService = {
  /**
   * Registra un nuevo usuario
   * @param {Object} data - Datos del usuario
   * @returns {Promise} Promesa con la respuesta del servidor
   */
  register(data) {
    return apiClient.post('/api/api-register/', data);
  },

  /**
   * Inicia sesión con credenciales
   * @param {Object} credentials - Credenciales (email, password)
   * @returns {Promise} Promesa con la respuesta del servidor
   */
  async login(credentials) {
    try {
      const response = await apiClient.post('/api/api-login/', credentials);
      
      // Si el login es exitoso y tenemos un token
      if (response.data.token) {
        tokenManager.setToken(
          response.data.token, 
          response.data.expires_in || 86400
        );
      }
      
      return response;
    } catch (error) {
      // Mejorar el manejo de errores específicos
      if (error.response) {
        const status = error.response.status;
        const data = error.response.data;
        
        // Crear un error más descriptivo
        const enhancedError = new Error();
        enhancedError.response = error.response;
        enhancedError.status = status;
        enhancedError.data = data;
        
        // Añadir información adicional según el tipo de error
        switch (status) {
          case 401:
            enhancedError.message = 'Credenciales incorrectas';
            enhancedError.type = 'INVALID_CREDENTIALS';
            break;
          case 403:
            enhancedError.message = 'Cuenta no activada o acceso denegado';
            enhancedError.type = 'ACCESS_DENIED';
            break;
          case 429:
            enhancedError.message = 'Demasiados intentos de inicio de sesión';
            enhancedError.type = 'RATE_LIMIT_EXCEEDED';
            break;
          default:
            enhancedError.message = error.message || 'Error de autenticación';
            enhancedError.type = 'AUTH_ERROR';
        }
        
        throw enhancedError;
      }
      
      // Re-lanzar el error original si no es un error de respuesta HTTP
      throw error;
    }
  },

  /**
   * Activa una cuenta con el token de activación
   * @param {string} uidb64 - ID del usuario codificado
   * @param {string} token - Token de activación
   * @returns {Promise} Promesa con la respuesta del servidor
   */
  activate(uidb64, token) {
    return apiClient.get(`/api/api-activate/${uidb64}/${token}/`);
  },

  /**
   * Reenvía el email de activación
   * @param {string} email - Email del usuario
   * @returns {Promise} Promesa con la respuesta del servidor
   */
  resendActivation(email) {
    return apiClient.post('/api/api-resend-activation/', { email });
  },

  /**
   * Cierra la sesión del usuario
   */
  logout() {
    try {
      // Intentar hacer logout en el servidor si hay token
      const token = tokenManager.getToken();
      if (token) {
        // Opcional: llamar al endpoint de logout del servidor
        apiClient.post('/api/api-logout/').catch(() => {
          // Ignorar errores del logout del servidor
          console.warn('Error al hacer logout en el servidor, continuando con logout local');
        });
      }
    } finally {
      // Siempre limpiar el token local
      tokenManager.clearToken();
    }
  },

  /**
   * Obtiene los datos del dashboard
   * @returns {Promise} Promesa con la respuesta del servidor
   */
  getDashboard() {
    return apiClient.get('/api/api-dashboard/');
  },

  /**
   * Verifica si el usuario está autenticado
   * @returns {boolean} True si hay un token válido
   */
  isAuthenticated() {
    return tokenManager.hasValidToken();
  },

  /**
   * Obtiene el token actual
   * @returns {string|null} Token actual o null si no existe
   */
  getCurrentToken() {
    return tokenManager.getToken();
  }
};