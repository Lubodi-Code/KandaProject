<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useRoomStore } from '../../stores/storytelling';
import { characterService } from '../../api/characters';

const router = useRouter();
const route = useRoute();
const roomStore = useRoomStore();
const currentUser = JSON.parse(localStorage.getItem('user') || '{}');

const myCharacters = ref([]);
const selectedCharacters = ref([]);
const loading = ref(false);

// Props
const roomId = route.params.id;

// Computed
const isAdmin = computed(() => {
  if (!roomStore.currentRoom) return false;
  return roomStore.currentRoom.admin === currentUser.id;
});

const canStartGame = computed(() => {
  return (
    isAdmin.value &&
    roomStore.currentRoom?.status === 'waiting' &&
    roomStore.participants.length > 0 &&
    roomStore.participants.every(p => p.is_ready)
  );
});

const myParticipant = computed(() => {
  return roomStore.participants.find(p => p.user === currentUser.id);
});

// Methods
const loadRoomData = async () => {
  try {
    loading.value = true;
    await Promise.all([
      roomStore.fetchRoom(roomId),
      roomStore.fetchParticipants(roomId),
      loadMyCharacters()
    ]);
  } catch (error) {
    console.error('Error loading room data:', error);
  } finally {
    loading.value = false;
  }
};

const loadMyCharacters = async () => {
  try {
    const response = await characterService.list();
    myCharacters.value = response.data;
  } catch (error) {
    console.error('Error loading characters:', error);
  }
};

const addCharacterToSelection = (character) => {
  if (!selectedCharacters.value.find(c => c.id === character.id)) {
    selectedCharacters.value.push(character);
  }
};

const removeCharacterFromSelection = (characterId) => {
  selectedCharacters.value = selectedCharacters.value.filter(c => c.id !== characterId);
};

const joinRoomWithCharacters = async () => {
  if (selectedCharacters.value.length === 0) {
    alert('Debes seleccionar al menos un personaje');
    return;
  }

  // Temporary: limit to 1 character per player to match current server logic
  if (selectedCharacters.value.length > 1) {
    alert('Por ahora solo puedes elegir 1 personaje para jugar.');
    selectedCharacters.value = selectedCharacters.value.slice(0, 1);
  }

  try {
    loading.value = true;
    const characterIds = selectedCharacters.value.map(c => c.id);
    await roomStore.addCharactersToRoom(roomId, characterIds);
    await roomStore.fetchParticipants(roomId);
  } catch (error) {
    console.error('Error joining room with characters:', error);
  } finally {
    loading.value = false;
  }
};

const startGame = async () => {
  if (!canStartGame.value) return;
  
  try {
    loading.value = true;
    await roomStore.startGame(roomId);
    router.push(`/game/${roomId}`);
  } catch (error) {
    console.error('Error starting game:', error);
  } finally {
    loading.value = false;
  }
};

const toggleReady = async () => {
  if (!myParticipant.value) return;
  try {
    loading.value = true;
    await roomStore.setParticipantReady(myParticipant.value.id, !myParticipant.value.is_ready);
    await roomStore.fetchParticipants(roomId);
  } catch (error) {
    console.error('Error toggling ready:', error);
  } finally {
    loading.value = false;
  }
};

const leaveRoom = async () => {
  if (confirm('-+Est+ís seguro de que quieres salir de esta sala?')) {
    try {
      await roomStore.leaveRoom(roomId);
      router.push('/dashboard');
    } catch (error) {
      console.error('Error leaving room:', error);
    }
  }
};

const copyAccessCode = () => {
  if (roomStore.currentRoom?.access_code) {
    navigator.clipboard.writeText(roomStore.currentRoom.access_code);
    // Aqu+¡ podr+¡as a+¦adir una notificaci+¦n de +®xito
  }
};

onMounted(() => {
  loadRoomData();
});
</script>

<template>
  <div class="p-4 max-w-6xl mx-auto">
    <!-- Loading state -->
    <div v-if="loading && !roomStore.currentRoom" class="text-center py-8">
      <p class="text-gray-500">Cargando sala...</p>
    </div>

    <!-- Room content -->
    <div v-else-if="roomStore.currentRoom">
      <!-- Header -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h1 class="text-3xl font-bold text-gray-800 mb-2">{{ roomStore.currentRoom.name }}</h1>
            <p class="text-gray-600">{{ roomStore.currentRoom.description || 'Sin descripci+¦n' }}</p>
          </div>
          <span
            :class="[
              'px-3 py-1 rounded-full text-sm font-medium',
              roomStore.currentRoom.status === 'waiting' 
                ? 'bg-green-100 text-green-800' 
                : roomStore.currentRoom.status === 'playing'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-800'
            ]"
          >
            {{ 
              roomStore.currentRoom.status === 'waiting' ? 'Esperando Jugadores' :
              roomStore.currentRoom.status === 'playing' ? 'Juego en Progreso' :
              'Finalizada'
            }}
          </span>
        </div>

        <!-- Room info -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span class="font-medium">Universo:</span>
            <p class="text-gray-600">{{ roomStore.currentRoom.universe_name }}</p>
          </div>
          <div>
            <span class="font-medium">Admin:</span>
            <p class="text-gray-600">{{ roomStore.currentRoom.admin_username }}</p>
          </div>
          <div>
            <span class="font-medium">Jugadores:</span>
            <p class="text-gray-600">{{ roomStore.currentRoom.player_count }}/{{ roomStore.currentRoom.max_players }}</p>
          </div>
          <div>
            <span class="font-medium">Cap+¡tulos:</span>
            <p class="text-gray-600">{{ roomStore.currentRoom.total_chapters }}</p>
          </div>
        </div>

        <!-- Access code for private rooms -->
        <div v-if="!roomStore.currentRoom.is_public && roomStore.currentRoom.access_code" class="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <div class="flex items-center justify-between">
            <div>
              <span class="font-medium text-yellow-800">C+¦digo de Acceso:</span>
              <span class="ml-2 font-mono text-lg text-yellow-900">{{ roomStore.currentRoom.access_code }}</span>
            </div>
            <button
              @click="copyAccessCode"
              class="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded text-sm transition-colors"
            >
              Copiar
            </button>
          </div>
          <p class="text-xs text-yellow-700 mt-1">Comparte este c+¦digo con otros jugadores para que se unan</p>
        </div>
      </div>

      <!-- Two column layout -->
      <div class="grid md:grid-cols-2 gap-6">
        <!-- Left column: Character selection -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold mb-4">Seleccionar Personajes</h2>
          <div v-if="roomStore.currentRoom?.status !== 'waiting'" class="p-3 mb-4 bg-gray-50 border border-gray-200 rounded text-sm text-gray-600">
            No puedes modificar personajes cuando la sala no est+í en estado "Esperando Jugadores".
          </div>
          
          <div v-if="myCharacters.length === 0" class="text-center py-8">
            <p class="text-gray-500 mb-4">No tienes personajes creados.</p>
            <button
              @click="router.push('/dashboard')"
              class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
            >
              Crear Personajes
            </button>
          </div>

          <div v-else>
            <!-- Available characters -->
            <div class="mb-6">
              <h3 class="font-medium mb-3">Mis Personajes Disponibles</h3>
              <div class="space-y-2 max-h-60 overflow-y-auto">
                <div
                  v-for="character in myCharacters"
                  :key="character.id"
                  class="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50"
                >
                  <div>
                    <p class="font-medium">{{ character.name }}</p>
                    <p class="text-sm text-gray-600">{{ character.archetype }} - {{ character.gender }}</p>
                  </div>
                  <button
                    @click="addCharacterToSelection(character)"
                    :disabled="roomStore.currentRoom?.status !== 'waiting' || selectedCharacters.find(c => c.id === character.id)"
                    class="bg-green-500 hover:bg-green-600 disabled:bg-gray-300 text-white px-3 py-1 rounded text-sm transition-colors"
                  >
                    {{ selectedCharacters.find(c => c.id === character.id) ? 'Seleccionado' : 'Seleccionar' }}
                  </button>
                </div>
              </div>
            </div>

            <!-- Selected characters -->
            <div class="mb-6">
              <h3 class="font-medium mb-3">Personajes Seleccionados ({{ selectedCharacters.length }})</h3>
              <div v-if="selectedCharacters.length === 0" class="text-gray-500 text-sm">
                No has seleccionado ning+¦n personaje a+¦n
              </div>
              <div v-else class="space-y-2">
                <div
                  v-for="character in selectedCharacters"
                  :key="character.id"
                  class="flex items-center justify-between p-3 bg-blue-50 border border-blue-200 rounded-lg"
                >
                  <div>
                    <p class="font-medium text-blue-900">{{ character.name }}</p>
                    <p class="text-sm text-blue-700">{{ character.archetype }} - {{ character.gender }}</p>
                  </div>
          <button
                    @click="removeCharacterFromSelection(character.id)"
                    class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm transition-colors"
                  >
                    Remover
                  </button>
                </div>
              </div>
            </div>

            <!-- Join button -->
            <button
              @click="joinRoomWithCharacters"
        :disabled="loading || selectedCharacters.length === 0 || roomStore.currentRoom?.status !== 'waiting'"
              class="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white px-4 py-3 rounded-lg font-medium transition-colors"
            >
              {{ loading ? 'Uni+®ndose...' : 'Unirse con Personajes Seleccionados' }}
            </button>
          </div>
        </div>

        <!-- Right column: Participants -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold mb-4">Participantes ({{ roomStore.participants.length }})</h2>
          
          <div v-if="roomStore.participants.length === 0" class="text-center py-8">
            <p class="text-gray-500">No hay participantes a+¦n.</p>
          </div>

          <div v-else class="space-y-4">
            <div
              v-for="participant in roomStore.participants"
              :key="participant.id"
              class="p-4 border rounded-lg"
            >
              <div class="flex items-center justify-between mb-2">
                <h3 class="font-medium">{{ participant.user_username }}</h3>
                <span
                  :class="[
                    'px-2 py-1 rounded-full text-xs',
                    participant.is_ready 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  ]"
                >
                  {{ participant.is_ready ? 'Listo' : 'Preparando' }}
                </span>
              </div>
              
              <div class="text-sm text-gray-600">
                <p><strong>Personajes:</strong> {{ participant.character_names.join(', ') || 'Ninguno' }}</p>
              </div>

              <!-- Ready toggle for my participant -->
              <div v-if="participant.user === currentUser.id" class="mt-3">
                <button
                  @click="toggleReady"
                  :disabled="loading"
                  :class="[
                    'px-4 py-1 rounded text-sm font-medium transition-colors',
                    participant.is_ready 
                      ? 'bg-gray-500 hover:bg-gray-600 text-white' 
                      : 'bg-green-500 hover:bg-green-600 text-white'
                  ]"
                >
                  {{ participant.is_ready ? 'Cancelar listo' : 'Estoy listo' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action buttons -->
      <div class="mt-6 flex justify-between">
        <button
          @click="leaveRoom"
          class="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg transition-colors"
        >
          Salir de la Sala
        </button>

        <div class="space-x-3">
          <button
            @click="router.push('/dashboard')"
            class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg transition-colors"
          >
            Volver al Dashboard
          </button>
          
          <!-- Start game button (admin only) -->
          <button
            v-if="isAdmin && roomStore.currentRoom.status === 'waiting'"
            @click="startGame"
            :disabled="loading || !canStartGame"
            class="bg-green-500 hover:bg-green-600 disabled:bg-green-300 text-white px-6 py-2 rounded-lg font-medium transition-colors"
          >
            {{ loading ? 'Iniciando...' : 'Iniciar Juego' }}
          </button>
          <p v-if="isAdmin && roomStore.currentRoom.status === 'waiting' && !canStartGame" class="text-xs text-gray-500 inline-block ml-2">
            Todos los jugadores deben estar listos
          </p>
          
          <!-- Continue game button -->
          <button
            v-if="roomStore.currentRoom.status === 'playing'"
            @click="router.push(`/game/${roomId}`)"
            class="bg-purple-500 hover:bg-purple-600 text-white px-6 py-2 rounded-lg transition-colors"
          >
            Continuar Juego
          </button>
        </div>
      </div>
    </div>

    <!-- Error state -->
    <div v-else-if="roomStore.error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      <p>{{ roomStore.error }}</p>
      <button
        @click="roomStore.clearError(); loadRoomData()"
        class="mt-2 text-sm underline"
      >
        Reintentar
      </button>
    </div>
  </div>
</template>
