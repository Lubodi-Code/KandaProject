<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

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
        <!-- Icono de correo -->
        <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-indigo-900/50 mb-6">
          <svg class="h-10 w-10 text-indigo-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>
        
        <!-- Título y mensaje -->
        <h2 class="text-3xl font-extrabold text-white mb-4">¡Revisa tu correo!</h2>
        <div class="rounded-md bg-indigo-900/30 p-4 border-l-4 border-indigo-500 mb-6">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-indigo-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-indigo-200">
                Hemos enviado un correo electrónico con un enlace de activación a tu dirección de correo. 
                Por favor, revisa tu bandeja de entrada y sigue las instrucciones para activar tu cuenta.
              </p>
            </div>
          </div>
        </div>
        
        <p class="text-gray-400 text-sm mb-6">
          Si no recibes el correo en unos minutos, revisa tu carpeta de spam o solicita un nuevo enlace de activación.
        </p>
        
        <!-- Botones de acción -->
        <div class="flex flex-col space-y-4">
          <button @click="goToResendActivation" 
                  class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200">
            Reenviar correo de activación
          </button>
          
          <button @click="goToLogin" 
                  class="w-full flex justify-center py-2 px-4 border border-gray-700 rounded-md shadow-sm text-sm font-medium text-gray-300 bg-gray-800 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200">
            Volver al inicio de sesión
          </button>
        </div>
      </div>
    </div>
  </div>
</template>