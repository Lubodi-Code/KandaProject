<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useRoomStore } from '../../stores/storytelling';

const router = useRouter();
const roomStore = useRoomStore();

const accessCode = ref('');
const loading = ref(false);
const error = ref('');

const joinWithCode = async () => {
  if (!accessCode.value.trim()) {
    error.value = 'Por favor ingresa un c+¦digo de acceso';
    return;
  }

  try {
    loading.value = true;
    error.value = '';
    
    const room = await roomStore.joinRoomWithCode(accessCode.value.trim().toUpperCase());
    router.push(`/rooms/${room.id}`);
  } catch (err) {
    error.value = roomStore.error || 'Error al unirse a la sala';
  } finally {
    loading.value = false;
  }
};

const goBack = () => {
  router.back();
};
</script>

<template>
  <div class="p-4 max-w-md mx-auto">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Unirse con C+¦digo</h1>
      <button
        @click="goBack"
        class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors"
      >
        Volver
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-md p-6">
      <div class="text-center mb-6">
        <p class="text-gray-600">
          Ingresa el c+¦digo de 6 caracteres que te proporcion+¦ el administrador de la sala
        </p>
      </div>

      <form @submit.prevent="joinWithCode" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            C+¦digo de Acceso
          </label>
          <input
            v-model="accessCode"
            type="text"
            :class="[
              'w-full px-4 py-3 text-center text-lg font-mono border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
              error ? 'border-red-500' : 'border-gray-300'
            ]"
            placeholder="ABC123"
            maxlength="6"
            style="text-transform: uppercase"
            @input="accessCode = accessCode.toUpperCase()"
          />
        </div>

        <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {{ error }}
        </div>

        <button
          type="submit"
          :disabled="loading || !accessCode.trim()"
          class="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white px-4 py-3 rounded-lg font-medium transition-colors"
        >
          {{ loading ? 'Uni+®ndose...' : 'Unirse a la Sala' }}
        </button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-sm text-gray-500 mb-3">
          -+No tienes un c+¦digo? Puedes:
        </p>
        <div class="space-y-2">
          <button
            @click="router.push('/rooms/public')"
            class="block w-full bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Ver Salas P+¦blicas
          </button>
          <button
            @click="router.push('/rooms/create')"
            class="block w-full bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Crear Nueva Sala
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
