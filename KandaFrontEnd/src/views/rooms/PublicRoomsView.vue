<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useRoomStore } from '../../stores/storytelling';

const router = useRouter();
const roomStore = useRoomStore();

const loading = ref(false);

const joinRoom = async (room) => {
  try {
    loading.value = true;
    await roomStore.joinRoom(room.id);
    router.push(`/rooms/${room.id}`);
  } catch (error) {
    console.error('Error joining room:', error);
  } finally {
    loading.value = false;
  }
};

const refreshRooms = async () => {
  await roomStore.fetchPublicRooms();
};

onMounted(() => {
  roomStore.fetchPublicRooms();
});
</script>

<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Salas P+在licas</h1>
      <div class="space-x-3">
        <button
          @click="refreshRooms"
          class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors"
        >
          Actualizar
        </button>
        <button
          @click="router.push('/dashboard')"
          class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
        >
          Volver al Dashboard
        </button>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="roomStore.loading" class="text-center py-8">
      <p class="text-gray-500">Cargando salas...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="roomStore.error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{{ roomStore.error }}</p>
      <button
        @click="roomStore.clearError(); refreshRooms()"
        class="mt-2 text-sm underline"
      >
        Reintentar
      </button>
    </div>

    <!-- Empty state -->
    <div v-else-if="roomStore.availableRooms.length === 0" class="text-center py-8">
      <p class="text-gray-500 mb-4">No hay salas p+在licas disponibles en este momento.</p>
      <button
        @click="router.push('/rooms/create')"
        class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors"
      >
        Crear la primera sala
      </button>
    </div>

    <!-- Rooms grid -->
    <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="room in roomStore.availableRooms"
        :key="room.id"
        class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
      >
        <div class="mb-4">
          <h3 class="text-lg font-semibold mb-2">{{ room.name }}</h3>
          <p class="text-gray-600 text-sm mb-2">{{ room.description || 'Sin descripci+好' }}</p>
          
          <div class="space-y-1 text-sm text-gray-500">
            <p><strong>Universo:</strong> {{ room.universe_name }}</p>
            <p><strong>Admin:</strong> {{ room.admin_username }}</p>
            <p><strong>Jugadores:</strong> {{ room.player_count }}/{{ room.max_players }}</p>
            <p><strong>Cap+﹀ulos:</strong> {{ room.total_chapters }}</p>
            <p><strong>Discusi+好:</strong> {{ room.allow_discussion ? 'Habilitada' : 'Deshabilitada' }}</p>
          </div>
        </div>

        <div class="flex justify-between items-center">
          <div class="flex items-center space-x-2">
            <span
              :class="[
                'px-2 py-1 rounded-full text-xs font-medium',
                room.status === 'waiting' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-yellow-100 text-yellow-800'
              ]"
            >
              {{ room.status === 'waiting' ? 'Esperando' : 'En Juego' }}
            </span>
          </div>
          
          <button
            @click="joinRoom(room)"
            :disabled="loading || room.player_count >= room.max_players"
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-colors',
              room.player_count >= room.max_players
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-500 hover:bg-blue-600 text-white'
            ]"
          >
            <span v-if="loading">Uni+峪dose...</span>
            <span v-else-if="room.player_count >= room.max_players">Sala Llena</span>
            <span v-else>Unirse</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="mt-8 text-center">
      <button
        @click="router.push('/rooms/create')"
        class="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg transition-colors"
      >
        Crear Nueva Sala
      </button>
    </div>
  </div>
</template>
