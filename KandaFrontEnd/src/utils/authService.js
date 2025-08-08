// authService.js
import { ref, onMounted } from 'vue';
import { authService } from '../api/auth';
import { characterService } from '../api/characters';

export const useAuth = () => {
  const isAuthenticated = ref(false);
  const isLoading = ref(true);
  const authError = ref(null);
  const connectionError = ref(null);

  // Verificar el estado de la conexi+好 y la autenticaci+好
  const checkAuthStatus = async () => {
    isLoading.value = true;
    authError.value = null;
    connectionError.value = null;

    try {
      // Primero verificar la conexi+好 con el backend
      console.log('[AUTH] Verificando conexi+好 con el backend...');
      const connected = await characterService.testConnection();
      
      if (!connected) {
        console.error('[AUTH] No se pudo conectar con el backend');
        connectionError.value = 'No se pudo conectar con el servidor. Verifica tu conexi+好 a internet.';
        isAuthenticated.value = false;
        return;
      }
      
      console.log('[AUTH] Conexi+好 exitosa, verificando autenticaci+好...');
      
      // Verificar si hay un token
      const hasToken = authService.isAuthenticated();
      
      if (!hasToken) {
        console.log('[AUTH] No hay token almacenado localmente');
        isAuthenticated.value = false;
        return;
      }
      
      // Verificar si el token es v+璱ido en el backend
      const authResult = await authService.checkAuth();
      console.log('[AUTH] Resultado de verificaci+好:', authResult);
      
      isAuthenticated.value = authResult.authenticated === true;
      
      if (!isAuthenticated.value && authResult.status === 'expired_token') {
        authError.value = 'Tu sesi+好 ha expirado. Por favor, inicia sesi+好 nuevamente.';
        authService.logout(); // Limpiar el token expirado
      } else if (!isAuthenticated.value) {
        authError.value = authResult.message || 'Sesi+好 no v+璱ida';
      }
      
    } catch (error) {
      console.error('[AUTH] Error al verificar estado de autenticaci+好:', error);
      authError.value = 'Error al verificar el estado de la sesi+好';
    } finally {
      isLoading.value = false;
    }
  };
  
  // Iniciar sesi+好
  const login = async (credentials) => {
    isLoading.value = true;
    authError.value = null;
    
    try {
      const response = await authService.login(credentials);
      isAuthenticated.value = true;
      return response;
    } catch (error) {
      console.error('[AUTH] Error de login:', error);
      authError.value = error.message || 'Error al iniciar sesi+好';
      throw error;
    } finally {
      isLoading.value = false;
    }
  };
  
  // Cerrar sesi+好
  const logout = () => {
    authService.logout();
    isAuthenticated.value = false;
  };
  
  // Verificar estado al montar el componente
  onMounted(() => {
    checkAuthStatus();
  });
  
  return {
    isAuthenticated,
    isLoading,
    authError,
    connectionError,
    checkAuthStatus,
    login,
    logout
  };
};
