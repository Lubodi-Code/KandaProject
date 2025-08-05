<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { authService } from '../../api/auth';
import tokenManager from '../../utils/tokenManager';

const router = useRouter();
const user = ref(null);
const isLoading = ref(true);
const error = ref(null);

// Obtener datos del usuario al montar el componente
onMounted(async () => {
  try {
    isLoading.value = true;
    const response = await authService.getDashboard();
    user.value = response.data;
  } catch (err) {
    console.error('Error al cargar el dashboard:', err);
    error.value = 'No se pudieron cargar los datos del usuario. Por favor, inténtalo de nuevo más tarde.';
    
    // Si hay un error de autenticación, redirigir al login
    if (err.response && (err.response.status === 401 || err.response.status === 403)) {
  
      logout();
    }
  } finally {
    isLoading.value = false;
  }
});

// Cerrar sesión
const logout = () => {
  tokenManager.clearToken();
  router.push('/login');
};
</script>

<template>
  <div class="min-h-screen bg-gray-900 text-white">
    <!-- Barra de navegación -->
    <nav class="bg-gray-800 border-b border-indigo-500/30 shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <div class="text-xl font-bold text-indigo-400">Kanda</div>
          </div>
          <div class="flex items-center">
            <button @click="logout" 
                    class="ml-4 px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200">
              Cerrar sesión
            </button>
          </div>
        </div>
      </div>
    </nav>
    
    <!-- Contenido principal -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="border-4 border-dashed border-indigo-500/30 rounded-lg p-6 bg-gray-800">
          <!-- Estado de carga -->
          <div v-if="isLoading" class="flex justify-center items-center h-64">
            <svg class="animate-spin h-10 w-10 text-indigo-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
          
          <!-- Error -->
          <div v-else-if="error" class="flex flex-col items-center justify-center h-64">
            <div class="text-red-400 text-xl mb-4">
              <svg class="h-12 w-12 mx-auto mb-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              {{ error }}
            </div>
            <button @click="router.go(0)" 
                    class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200">
              Reintentar
            </button>
          </div>
          
          <!-- Datos del usuario -->
          <div v-else-if="user" class="space-y-6">
            <h1 class="text-2xl font-bold text-indigo-400 mb-6">Bienvenido, {{ user.username }}</h1>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Información del usuario -->
              <div class="bg-gray-900 p-6 rounded-lg border border-indigo-500/30 shadow-lg">
                <h2 class="text-xl font-semibold text-indigo-300 mb-4">Información de la cuenta</h2>
                <div class="space-y-4">
                  <div>
                    <p class="text-gray-400 text-sm">Nombre de usuario</p>
                    <p class="text-white font-medium">{{ user.username }}</p>
                  </div>
                  <div>
                    <p class="text-gray-400 text-sm">Correo electrónico</p>
                    <p class="text-white font-medium">{{ user.email }}</p>
                  </div>
                  <div>
                    <p class="text-gray-400 text-sm">Estado de la cuenta</p>
                    <p class="text-green-400 font-medium flex items-center">
                      <svg class="h-5 w-5 mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                      </svg>
                      Activa
                    </p>
                  </div>
                  <div>
                    <p class="text-gray-400 text-sm">Fecha de registro</p>
                    <p class="text-white font-medium">{{ new Date(user.date_joined).toLocaleDateString() }}</p>
                  </div>
                </div>
              </div>
              
              <!-- Estadísticas o información adicional -->
              <div class="bg-gray-900 p-6 rounded-lg border border-indigo-500/30 shadow-lg">
                <h2 class="text-xl font-semibold text-indigo-300 mb-4">Actividad reciente</h2>
                <div class="flex items-center justify-center h-40 text-gray-500">
                  <p>No hay actividad reciente para mostrar</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>