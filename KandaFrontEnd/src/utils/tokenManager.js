/**
 * M贸dulo para gestionar tokens de autenticaci贸n
 */

const TOKEN_KEY = 'auth_token';
const TOKEN_TIMESTAMP_KEY = 'auth_token_timestamp';
const TOKEN_EXPIRY_KEY = 'auth_token_expiry';

export default {
  /**
   * Guarda el token de autenticaci贸n en localStorage
   * @param {string} token - Token de autenticaci贸n
   * @param {number} expiresIn - Tiempo de expiraci贸n en segundos
   */
  setToken(token, expiresIn = 86400) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(TOKEN_TIMESTAMP_KEY, Date.now().toString());
    localStorage.setItem(TOKEN_EXPIRY_KEY, expiresIn.toString());
    console.debug(`[Token] Token guardado, expira en ${expiresIn} segundos`);
  },

  /**
   * Obtiene el token de autenticaci贸n
   * @returns {string|null} Token de autenticaci贸n o null si no existe
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
    const timeLeft = (tokenTime + expirySeconds - now) / 1000; // segundos restantes
    
    // Depuraci+ de tiempo restante
    if (timeLeft > 0) {
      console.debug(`[Token] Token v+韑ido, expira en ${Math.floor(timeLeft)} segundos`);
    }
    
    return now - tokenTime > expirySeconds;
  },

  /**
   * Verifica si el usuario est谩 autenticado
   * @returns {boolean} True si el usuario est谩 autenticado, false en caso contrario
   */
  isAuthenticated() {
    return this.getToken() !== null && !this.isTokenExpired();
  },

  /**
   * Elimina el token de autenticaci贸n
   */
  clearToken() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(TOKEN_TIMESTAMP_KEY);
    localStorage.removeItem(TOKEN_EXPIRY_KEY);
    console.debug('[Token] Token eliminado');
  }
};