<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { authService } from '../../api/auth';

const route = useRoute();
const router = useRouter();

const status = ref('loading'); // loading, success, error
const message = ref('');
const justRegistered = ref(route.query.justRegistered === 'true');

// Activar la cuenta al cargar el componente
onMounted(async () => {
  const { uidb64, token } = route.params;
  
  if (!uidb64 || !token) {
    status.value = 'error';
    message.value = 'Enlace de activación inválido. Faltan parámetros necesarios.';
    return;
  }
  
  try {
    const response = await authService.activate(uidb64, token);
    status.value = 'success';
    message.value = response.data.message || 'Tu cuenta ha sido activada correctamente. Ya puedes iniciar sesión.';
  } catch (error) {
    status.value = 'error';
    if (error.response && error.response.data && error.response.data.error) {
      message.value = error.response.data.error;
    } else {
      message.value = 'Error al activar la cuenta. El enlace puede ser inválido o haber expirado.';
    }
    console.error('Error de activación:', error);
  }
});

// Ir a la página de login
const goToLogin = () => {
  router.push('/login');
};

// Ir a la página de reenvío de activación
const goToResendActivation = () => {
  router.push('/resend-activation');
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8" 
       style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);">
    <div class="max-w-md w-full space-y-8 bg-gray-900 p-8 rounded-xl shadow-2xl border border-indigo-500/30">
      <div class="text-center">
        <h2 class="mt-6 text-3xl font-extrabold text-white">Activación de cuenta</h2>
        <p v-if="justRegistered" class="mt-2 text-sm text-indigo-300">
          Gracias por registrarte. Revisa tu correo electrónico para activar tu cuenta.
        </p>
      </div>
      
      <!-- Estado de carga -->
      <div v-if="status === 'loading'" class="flex flex-col items-center justify-center py-6">
        <div class="animate-spin h-12 w-12 border-t-2 border-b-2 border-indigo-500 rounded-full mb-4"></div>
        <p class="text-center text-gray-300">Verificando tu enlace de activación...</p>
      </div>
      
      <!-- Estado de éxito -->
      <div v-else-if="status === 'success'" class="flex flex-col items-center justify-center py-6">
        <div class="flex items-center justify-center mb-6 bg-indigo-900/50 rounded-full h-20 w-20 border border-indigo-500">
          <svg class="h-10 w-10 text-indigo-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        
        <h3 class="text-xl font-medium text-white mb-2">¡Cuenta activada!</h3>
        <p class="text-center text-gray-300 mb-6">{{ message }}</p>
        
        <button @click="goToLogin" 
                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200 transform hover:scale-105">
          Ir a iniciar sesión
        </button>
      </div>
      
      <!-- Estado de error -->
      <div v-else class="flex flex-col items-center justify-center py-6">
        <div class="flex items-center justify-center mb-6 bg-red-900/30 rounded-full h-20 w-20 border border-red-500">
          <svg class="h-10 w-10 text-red-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        
        <h3 class="text-xl font-medium text-white mb-2">Error de activación</h3>
        <p class="text-center text-gray-300 mb-6">{{ message }}</p>
        
        <div class="flex flex-col space-y-4 w-full">
          <button @click="goToResendActivation" 
                  class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200 transform hover:scale-105">
            Solicitar un nuevo enlace
          </button>
          
          <button @click="goToLogin" 
                  class="w-full flex justify-center py-2 px-4 border border-indigo-300 rounded-md shadow-sm text-sm font-medium text-indigo-300 bg-transparent hover:bg-indigo-900/30 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200">
            Volver a iniciar sesión
          </button>
        </div>
      </div>
    </div>
  </div>
</template>