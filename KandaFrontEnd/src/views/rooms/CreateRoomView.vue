<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUniverseStore, useRoomStore } from '../../stores/storytelling';

const router = useRouter();
const universeStore = useUniverseStore();
const roomStore = useRoomStore();

const form = ref({
  name: '',
  description: '',
  universe: '',
  is_public: true,
  max_players: 6,
  total_chapters: 5,
  discussion_time: 300,
  allow_discussion: true
});

const errors = ref({});
const loading = ref(false);

const validateForm = () => {
  const newErrors = {};
  
  if (!form.value.name.trim()) {
    newErrors.name = 'El nombre de la sala es requerido';
  }
  
  if (!form.value.universe) {
    newErrors.universe = 'Debes seleccionar un universo';
  }
  
  if (form.value.max_players < 1 || form.value.max_players > 20) {
    newErrors.max_players = 'El n+¦mero de jugadores debe estar entre 1 y 20';
  }
  
  if (form.value.total_chapters < 1 || form.value.total_chapters > 100) {
    newErrors.total_chapters = 'El n+¦mero de cap+¡tulos debe estar entre 1 y 100';
  }

  if (form.value.discussion_time < 60 || form.value.discussion_time > 1800) {
    newErrors.discussion_time = 'El tiempo de discusi+¦n debe estar entre 1 y 30 minutos';
  }
  
  errors.value = newErrors;
  return Object.keys(newErrors).length === 0;
};

const createRoom = async () => {
  if (!validateForm()) return;
  
  try {
    loading.value = true;
    const roomData = {
      ...form.value,
      discussion_time: form.value.allow_discussion ? form.value.discussion_time : 0
    };
    
    const newRoom = await roomStore.createRoom(roomData);
    router.push(`/rooms/${newRoom.id}`);
  } catch (error) {
    console.error('Error creating room:', error);
  } finally {
    loading.value = false;
  }
};

const goBack = () => {
  router.back();
};

onMounted(() => {
  universeStore.fetchUniverses();
});
</script>

<template>
  <div class="p-4 max-w-2xl mx-auto">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Crear Nueva Sala</h1>
      <button
        @click="goBack"
        class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors"
      >
        Volver
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-md p-6">
      <form @submit.prevent="createRoom" class="space-y-6">
        <!-- Informaci+¦n b+ísica -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Nombre de la Sala *
            </label>
            <input
              v-model="form.name"
              type="text"
              :class="[
                'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                errors.name ? 'border-red-500' : 'border-gray-300'
              ]"
              placeholder="Ej: Aventura +ëpica"
              maxlength="200"
            />
            <p v-if="errors.name" class="text-red-500 text-xs mt-1">{{ errors.name }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Universo *
            </label>
            <select
              v-model="form.universe"
              :class="[
                'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                errors.universe ? 'border-red-500' : 'border-gray-300'
              ]"
            >
              <option value="">Selecciona un universo</option>
              <option
                v-for="universe in universeStore.universes"
                :key="universe.id"
                :value="universe.id"
              >
                {{ universe.name }}
              </option>
            </select>
            <p v-if="errors.universe" class="text-red-500 text-xs mt-1">{{ errors.universe }}</p>
          </div>
        </div>

        <!-- Descripci+¦n -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Descripci+¦n
          </label>
          <textarea
            v-model="form.description"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Describe brevemente de qu+® tratar+í esta partida..."
            maxlength="500"
          ></textarea>
        </div>

        <!-- Configuraci+¦n de acceso -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-3">
            Tipo de Sala
          </label>
          <div class="space-y-2">
            <label class="flex items-center">
              <input
                v-model="form.is_public"
                type="radio"
                :value="true"
                class="text-blue-600 focus:ring-blue-500"
              />
              <span class="ml-2">P+¦blica (visible para todos)</span>
            </label>
            <label class="flex items-center">
              <input
                v-model="form.is_public"
                type="radio"
                :value="false"
                class="text-blue-600 focus:ring-blue-500"
              />
              <span class="ml-2">Privada (solo con c+¦digo de acceso)</span>
            </label>
          </div>
        </div>

        <!-- Configuraci+¦n del juego -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              M+íximo de Jugadores
            </label>
            <input
              v-model.number="form.max_players"
              type="number"
              min="1"
              max="20"
              :class="[
                'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                errors.max_players ? 'border-red-500' : 'border-gray-300'
              ]"
            />
            <p v-if="errors.max_players" class="text-red-500 text-xs mt-1">{{ errors.max_players }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              N+¦mero de Cap+¡tulos
            </label>
            <input
              v-model.number="form.total_chapters"
              type="number"
              min="1"
              max="100"
              :class="[
                'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                errors.total_chapters ? 'border-red-500' : 'border-gray-300'
              ]"
            />
            <p v-if="errors.total_chapters" class="text-red-500 text-xs mt-1">{{ errors.total_chapters }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Tiempo de Discusi+¦n (segundos)
            </label>
            <input
              v-model.number="form.discussion_time"
              type="number"
              min="60"
              max="1800"
              :disabled="!form.allow_discussion"
              :class="[
                'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                !form.allow_discussion ? 'bg-gray-100' : '',
                errors.discussion_time ? 'border-red-500' : 'border-gray-300'
              ]"
            />
            <p v-if="errors.discussion_time" class="text-red-500 text-xs mt-1">{{ errors.discussion_time }}</p>
          </div>
        </div>

        <!-- Configuraci+¦n de discusi+¦n -->
        <div>
          <label class="flex items-center">
            <input
              v-model="form.allow_discussion"
              type="checkbox"
              class="text-blue-600 focus:ring-blue-500"
            />
            <span class="ml-2 text-sm font-medium text-gray-700">
              Permitir discusiones entre cap+¡tulos
            </span>
          </label>
          <p class="text-xs text-gray-500 mt-1">
            Si est+í habilitado, los jugadores podr+ín proponer acciones entre cap+¡tulos
          </p>
        </div>

        <!-- Error general -->
        <div v-if="roomStore.error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {{ roomStore.error }}
        </div>

        <!-- Botones -->
        <div class="flex justify-end space-x-3">
          <button
            type="button"
            @click="goBack"
            class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg transition-colors"
          >
            Cancelar
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white px-6 py-2 rounded-lg transition-colors"
          >
            {{ loading ? 'Creando...' : 'Crear Sala' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
