<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authService } from '../../api/auth';

const router = useRouter();

// Estado del formulario
const email = ref('');
const errors = ref({});
const isLoading = ref(false);
const resendSuccess = ref(false);

// Validar el formulario
const validateForm = () => {
  const newErrors = {};
  
  if (!email.value) {
    newErrors.email = 'El email es obligatorio';
  } else if (!/^\S+@\S+\.\S+$/.test(email.value)) {
    newErrors.email = 'El email no es válido';
  }
  
  errors.value = newErrors;
  return Object.keys(newErrors).length === 0;
};

// Enviar el formulario
const handleSubmit = async () => {
  if (!validateForm()) return;
  
  isLoading.value = true;
  errors.value = {};
  
  try {
    await authService.resendActivation(email.value);
    
    // Reenvío exitoso
    resendSuccess.value = true;
    email.value = '';
  } catch (error) {
    // Manejar errores de la API
    if (error.response && error.response.data) {
      const apiErrors = error.response.data;
      
      // Mapear errores de la API a nuestro formato
      if (apiErrors.error) {
        errors.value.general = apiErrors.error;
      } else {
        Object.keys(apiErrors).forEach(key => {
          errors.value[key] = Array.isArray(apiErrors[key]) 
            ? apiErrors[key][0] 
            : apiErrors[key];
        });
      }
      
      // Si hay un error no específico
      if (error.response.status === 400 && !Object.keys(errors.value).length) {
        errors.value.general = 'No se pudo reenviar el correo de activación. Inténtalo de nuevo.';
      }
    } else {
      errors.value.general = 'Error al reenviar el correo de activación. Inténtalo de nuevo.';
    }
  } finally {
    isLoading.value = false;
  }
};

// Ir a la página de login
const goToLogin = () => {
  router.push('/login');
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
        <h2 class="mt-6 text-3xl font-extrabold text-white">Reenviar correo de activación</h2>
      </div>
      
      <!-- Mensaje de éxito -->
      <div v-if="resendSuccess" class="rounded-md p-4 bg-indigo-900/30 border-l-4 border-indigo-500">
        <div class="flex">
          <div class="flex-shrink-0">
            <!-- Icono de check -->
            <svg class="h-5 w-5 text-indigo-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-indigo-300">Correo enviado</h3>
            <div class="mt-2 text-sm text-gray-300">
              <p>Hemos enviado un nuevo correo de activación a tu dirección de email. Por favor, revisa tu bandeja de entrada y sigue las instrucciones para activar tu cuenta.</p>
            </div>
            <div class="mt-4">
              <button @click="goToLogin" 
                      class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200 transform hover:scale-105">
                Ir a iniciar sesión
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Formulario -->
      <form v-else class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <!-- Error general -->
        <div v-if="errors.general" class="rounded-md bg-red-900/30 p-4 border-l-4 border-red-500">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-red-300">{{ errors.general }}</p>
            </div>
          </div>
        </div>
        
        <div class="rounded-md -space-y-px">
          <div>
            <label for="email" class="sr-only">Correo electrónico</label>
            <input id="email" 
                   name="email" 
                   type="email" 
                   autocomplete="email" 
                   required 
                   v-model="email"
                   class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-700 placeholder-gray-500 text-white bg-gray-800 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" 
                   placeholder="Correo electrónico" />
          </div>
          <p v-if="errors.email" class="mt-2 text-sm text-red-400">{{ errors.email }}</p>
        </div>
        
        <div>
          <button type="submit" 
                  :disabled="isLoading"
                  class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed">
            <span v-if="isLoading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="animate-spin h-5 w-5 text-indigo-300" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ isLoading ? 'Enviando...' : 'Enviar correo de activación' }}
          </button>
        </div>
        
        <div class="flex items-center justify-between">
          <div class="text-sm">
            <a @click="goToLogin" class="font-medium text-indigo-400 hover:text-indigo-300 cursor-pointer">
              ¿Ya tienes una cuenta? Inicia sesión
            </a>
          </div>
          <div class="text-sm">
            <a @click="goToRegister" class="font-medium text-indigo-400 hover:text-indigo-300 cursor-pointer">
              ¿No tienes cuenta? Regístrate
            </a>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>