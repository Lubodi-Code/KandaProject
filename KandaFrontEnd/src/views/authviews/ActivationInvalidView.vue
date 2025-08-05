<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

// Ir a la página de reenvío de activación
const goToResendActivation = () => {
  router.push('/resend-activation');
};

// Ir a la página de registro
const goToRegister = () => {
  router.push('/register');
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8" 
       style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);">
    <div class="max-w-md w-full space-y-8 bg-gray-900 p-8 rounded-xl shadow-2xl border border-indigo-500/30">
      <div class="text-center">
        <h2 class="mt-6 text-3xl font-extrabold text-white">Enlace inválido</h2>
      </div>
      
      <div class="flex flex-col items-center justify-center py-6">
        <div class="flex items-center justify-center mb-6 bg-red-900/30 rounded-full h-20 w-20 border border-red-500">
          <svg class="h-10 w-10 text-red-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        
        <h3 class="text-xl font-medium text-white mb-2">Enlace de activación inválido</h3>
        <p class="text-center text-gray-300 mb-6">
          El enlace de activación que has utilizado es inválido o ha expirado. 
          Por favor, solicita un nuevo enlace de activación o crea una nueva cuenta.
        </p>
        
        <div class="flex flex-col space-y-4 w-full">
          <button @click="goToResendActivation" 
                  class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200 transform hover:scale-105">
            Solicitar un nuevo enlace
          </button>
          
          <button @click="goToRegister" 
                  class="w-full flex justify-center py-2 px-4 border border-indigo-300 rounded-md shadow-sm text-sm font-medium text-indigo-300 bg-transparent hover:bg-indigo-900/30 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200">
            Crear una nueva cuenta
          </button>
        </div>
      </div>
    </div>
  </div>
</template>