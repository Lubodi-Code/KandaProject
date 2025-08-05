<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authService } from '../../api/auth';

const router = useRouter();

// Estado del formulario
const form = ref({
  email: '',
  password: ''
});

// Estado de errores y carga
const errors = ref({});
const isLoading = ref(false);

// Validar el formulario
const validateForm = () => {
  const newErrors = {};
  
  if (!form.value.email) {
    newErrors.email = 'El email es obligatorio';
  } else if (!/\S+@\S+\.\S+/.test(form.value.email)) {
    newErrors.email = 'El email no tiene un formato válido';
  }
  
  if (!form.value.password) {
    newErrors.password = 'La contraseña es obligatoria';
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
    await authService.login({
      email: form.value.email,
      password: form.value.password
    });
    
    // Login exitoso, redirigir al dashboard
    router.push('/dashboard');
  } catch (error) {
    console.error('Error de login:', error);
    
    // Manejar errores de la API
    if (error.response) {
      const status = error.response.status;
      const apiErrors = error.response.data;
      
      switch (status) {
        case 401:
          // Error de autenticación - credenciales incorrectas
          errors.value.general = 'Email o contraseña incorrectos';
          break;
        case 400:
          // Error de validación
          if (apiErrors.error) {
            errors.value.general = apiErrors.error;
          } else {
            // Mapear errores específicos de campo
            Object.keys(apiErrors).forEach(key => {
              errors.value[key] = Array.isArray(apiErrors[key]) 
                ? apiErrors[key][0] 
                : apiErrors[key];
            });
          }
          break;
        case 403:
          // Cuenta no activada
          errors.value.general = 'Tu cuenta no ha sido activada. Por favor, revisa tu correo electrónico.';
          break;
        case 429:
          // Demasiados intentos
          errors.value.general = 'Demasiados intentos de inicio de sesión. Por favor, inténtalo más tarde.';
          break;
        case 500:
          // Error del servidor
          errors.value.general = 'Error interno del servidor. Por favor, inténtalo más tarde.';
          break;
        default:
          errors.value.general = 'Error al iniciar sesión. Por favor, inténtalo de nuevo.';
      }
    } else if (error.request) {
      // Error de red - no se recibió respuesta
      errors.value.general = 'Error de conexión. Verifica tu conexión a internet e inténtalo de nuevo.';
    } else {
      // Error inesperado
      errors.value.general = 'Error inesperado. Por favor, inténtalo de nuevo.';
    }
  } finally {
    isLoading.value = false;
  }
};

// Ir a la página de registro
const goToRegister = () => {
  router.push('/register');
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
      <!-- Logo y título -->
      <div class="text-center">
        <h2 class="mt-6 text-3xl font-extrabold text-white">Iniciar sesión</h2>
        <p class="mt-2 text-sm text-gray-400">
          ¿No tienes una cuenta?
          <a @click="goToRegister" class="font-medium text-indigo-400 hover:text-indigo-300 cursor-pointer">
            Regístrate
          </a>
        </p>
      </div>
      
      <!-- Formulario -->
      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
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
          <!-- Email -->
          <div class="mb-4">
            <label for="email" class="block text-sm font-medium text-gray-300 mb-1">Correo electrónico</label>
            <input id="email" 
                   name="email" 
                   type="email" 
                   autocomplete="email" 
                   required 
                   v-model="form.email"
                   class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-700 placeholder-gray-500 text-white bg-gray-800 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" 
                   placeholder="tu@email.com" />
            <p v-if="errors.email" class="mt-2 text-sm text-red-400">{{ errors.email }}</p>
          </div>
          
          <!-- Contraseña -->
          <div class="mb-4">
            <label for="password" class="block text-sm font-medium text-gray-300 mb-1">Contraseña</label>
            <input id="password" 
                   name="password" 
                   type="password" 
                   autocomplete="current-password" 
                   required 
                   v-model="form.password"
                   class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-700 placeholder-gray-500 text-white bg-gray-800 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" 
                   placeholder="********" />
            <p v-if="errors.password" class="mt-2 text-sm text-red-400">{{ errors.password }}</p>
          </div>
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
            {{ isLoading ? 'Iniciando sesión...' : 'Iniciar sesión' }}
          </button>
        </div>
        
        <div class="text-center">
          <a @click="goToResendActivation" class="font-medium text-indigo-400 hover:text-indigo-300 cursor-pointer text-sm">
            ¿No has recibido el email de activación?
          </a>
        </div>
      </form>
    </div>
  </div>
</template>