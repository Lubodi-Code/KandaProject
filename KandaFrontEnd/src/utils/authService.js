// authService.js
import { ref, onMounted } from 'vue';
import { authService } from '../api/auth';
import { characterService } from '../api/characters';

export const useAuth = () => {
  const isAuthenticated = ref(false);
  const isLoading = ref(true);
  const authError = ref(null);
  const connectionError = ref(null);

  // Verificar el estado de la conexi+�n y la autenticaci+�n
  const checkAuthStatus = async () => {
    isLoading.value = true;
    authError.value = null;
    connectionError.value = null;

    try {
      // Primero verificar la conexi+�n con el backend
      console.log('[AUTH] Verificando conexi+�n con el backend...');
      const connected = await characterService.testConnection();
      
      if (!connected) {
        console.error('[AUTH] No se pudo conectar con el backend');
        connectionError.value = 'No se pudo conectar con el servidor. Verifica tu conexi+�n a internet.';
        isAuthenticated.value = false;
        return;
      }
      
      console.log('[AUTH] Conexi+�n exitosa, verificando autenticaci+�n...');
      
      // Verificar si hay un token
      const hasToken = authService.isAuthenticated();
      
      if (!hasToken) {
        console.log('[AUTH] No hay token almacenado localmente');
        isAuthenticated.value = false;
        return;
      }
      
      // Verificar si el token es v+�lido en el backend
      const authResult = await authService.checkAuth();
      console.log('[AUTH] Resultado de verificaci+�n:', authResult);
      
      isAuthenticated.value = authResult.authenticated === true;
      
      if (!isAuthenticated.value && authResult.status === 'expired_token') {
        authError.value = 'Tu sesi+�n ha expirado. Por favor, inicia sesi+�n nuevamente.';
        authService.logout(); // Limpiar el token expirado
      } else if (!isAuthenticated.value) {
        authError.value = authResult.message || 'Sesi+�n no v+�lida';
      }
      
    } catch (error) {
      console.error('[AUTH] Error al verificar estado de autenticaci+�n:', error);
      authError.value = 'Error al verificar el estado de la sesi+�n';
    } finally {
      isLoading.value = false;
    }
  };
  
  // Iniciar sesi+�n
  const login = async (credentials) => {
    isLoading.value = true;
    authError.value = null;
    
    try {
      const response = await authService.login(credentials);
      isAuthenticated.value = true;
      return response;
    } catch (error) {
      console.error('[AUTH] Error de login:', error);
      authError.value = error.message || 'Error al iniciar sesi+�n';
      throw error;
    } finally {
      isLoading.value = false;
    }
  };
  
  // Cerrar sesi+�n
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
