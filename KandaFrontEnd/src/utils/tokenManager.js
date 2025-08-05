/**
 * Módulo para gestionar tokens de autenticación
 */

const TOKEN_KEY = 'auth_token';
const TOKEN_TIMESTAMP_KEY = 'auth_token_timestamp';
const TOKEN_EXPIRY_KEY = 'auth_token_expiry';

export default {
  /**
   * Guarda el token de autenticación en localStorage
   * @param {string} token - Token de autenticación
   * @param {number} expiresIn - Tiempo de expiración en segundos
   */
  setToken(token, expiresIn = 86400) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(TOKEN_TIMESTAMP_KEY, Date.now().toString());
    localStorage.setItem(TOKEN_EXPIRY_KEY, expiresIn.toString());
  },

  /**
   * Obtiene el token de autenticación
   * @returns {string|null} Token de autenticación o null si no existe
   */
  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  /**
   * Verifica si el token ha expirado
   * @returns {boolean} True si el token ha expirado, false en caso contrario
   */
  isTokenExpired() {
    const timestamp = localStorage.getItem(TOKEN_TIMESTAMP_KEY);
    const expiry = localStorage.getItem(TOKEN_EXPIRY_KEY);
    
    if (!timestamp || !expiry) {
      return true;
    }
    
    const now = Date.now();
    const tokenTime = parseInt(timestamp, 10);
    const expirySeconds = parseInt(expiry, 10) * 1000; // Convertir a milisegundos
    
    return now - tokenTime > expirySeconds;
  },

  /**
   * Verifica si el usuario está autenticado
   * @returns {boolean} True si el usuario está autenticado, false en caso contrario
   */
  isAuthenticated() {
    return this.getToken() !== null && !this.isTokenExpired();
  },

  /**
   * Elimina el token de autenticación
   */
  clearToken() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(TOKEN_TIMESTAMP_KEY);
    localStorage.removeItem(TOKEN_EXPIRY_KEY);
    
  }
};