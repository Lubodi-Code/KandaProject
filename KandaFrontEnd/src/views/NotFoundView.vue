<script setup>
import { useRouter } from 'vue-router';
import tokenManager from '../utils/tokenManager';

const router = useRouter();

// Redirigir a la página principal según el estado de autenticación
const goToHome = () => {
  if (tokenManager.isAuthenticated()) {
    router.push('/dashboard');
  } else {
    router.push('/login');
  }
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 text-center">
      <div>
        <h1 class="text-9xl font-extrabold text-indigo-600">404</h1>
        <h2 class="mt-6 text-3xl font-bold text-gray-900">Página no encontrada</h2>
        <p class="mt-2 text-sm text-gray-600">
          Lo sentimos, la página que estás buscando no existe o ha sido movida.
        </p>
      </div>
      
      <div>
        <button @click="goToHome" class="btn-primary">
          Volver a la página principal
        </button>
      </div>
    </div>
  </div>
</template>