<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useRoomStore } from '../../stores/storytelling';

const router = useRouter();
const roomStore = useRoomStore();

const refreshRooms = async () => {
  await roomStore.fetchJoinedRooms();
};

const goToRoom = (roomId) => {
  router.push(`/rooms/${roomId}`);
};

const leaveRoom = async (room) => {
  if (confirm(`-+Est+ís seguro de que quieres salir de "${room.name}"?`)) {
    try {
      await roomStore.leaveRoom(room.id);
      await refreshRooms();
    } catch (error) {
      console.error('Error leaving room:', error);
    }
  }
};

onMounted(() => {
  roomStore.fetchJoinedRooms();
});
</script>

<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Salas Unidas</h1>
      <div class="space-x-3">
        <button
          @click="refreshRooms"
          class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors"
        >
          Actualizar
        </button>
        <button
          @click="router.push('/rooms/public')"
          class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors"
        >
          Buscar M+ís Salas
        </button>
        <button
          @click="router.push('/dashboard')"
          class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors"
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
    <div v-else-if="roomStore.joinedRooms.length === 0" class="text-center py-8">
      <p class="text-gray-500 mb-4">No te has unido a ninguna sala a+¦n.</p>
      <div class="space-y-2">
        <button
          @click="router.push('/rooms/public')"
          class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors mr-3"
        >
          Ver Salas P+¦blicas
        </button>
        <button
          @click="router.push('/rooms/join-private')"
          class="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg transition-colors"
        >
          Unirse con C+¦digo
        </button>
      </div>
    </div>

    <!-- Rooms grid -->
    <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="room in roomStore.joinedRooms"
        :key="room.id"
        class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
      >
        <div class="mb-4">
          <div class="flex justify-between items-start mb-2">
            <h3 class="text-lg font-semibold">{{ room.name }}</h3>
            <span
              :class="[
                'px-2 py-1 rounded-full text-xs font-medium',
                room.status === 'waiting' 
                  ? 'bg-green-100 text-green-800' 
                  : room.status === 'playing'
                  ? 'bg-blue-100 text-blue-800'
                  : 'bg-gray-100 text-gray-800'
              ]"
            >
              {{ 
                room.status === 'waiting' ? 'Esperando' :
                room.status === 'playing' ? 'En Juego' :
                'Finalizada'
              }}
            </span>
          </div>
          
          <p class="text-gray-600 text-sm mb-3">{{ room.description || 'Sin descripci+¦n' }}</p>
          
          <div class="space-y-1 text-sm text-gray-500">
            <p><strong>Universo:</strong> {{ room.universe_name }}</p>
            <p><strong>Admin:</strong> {{ room.admin_username }}</p>
            <p><strong>Jugadores:</strong> {{ room.player_count }}/{{ room.max_players }}</p>
            <p><strong>Cap+¡tulos:</strong> {{ room.total_chapters }}</p>
            <p><strong>Tipo:</strong> {{ room.is_public ? 'P+¦blica' : 'Privada' }}</p>
          </div>
        </div>

        <div class="space-y-2">
          <button
            @click="goToRoom(room.id)"
            class="w-full bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Ver Sala
          </button>
          
          <!-- Bot+¦n para continuar juego si est+í en progreso -->
          <button
            v-if="room.status === 'playing'"
            @click="router.push(`/game/${room.id}`)"
            class="w-full bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Continuar Juego
          </button>
          
          <!-- Bot+¦n para salir de la sala -->
          <button
            v-if="room.status === 'waiting'"
            @click="leaveRoom(room)"
            class="w-full bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Salir de la Sala
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
