<script setup>
import { ref, onMounted, nextTick, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useRoomStore } from '../../stores/storytelling';
import { storytellingService } from '../../api/storytelling';

const router = useRouter();
const route = useRoute();
const roomStore = useRoomStore();

const currentStory = ref(null);
const currentChapter = ref(null);
const chapters = ref([]);
const playerAction = ref('');
const isSubmittingAction = ref(false);
const aiResponse = ref('');
const isGeneratingResponse = ref(false);
const chatMessages = ref([]);
const newMessage = ref('');

// Props
const roomId = route.params.roomId || route.params.id;

// Computed
const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
const isPlayerTurn = computed(() => {
  // If turn handling isn't implemented server-side yet, allow action after narrative is generated
  if (!currentStory.value) return false;
  if (!('current_player' in currentStory.value)) return true; // fallback single-player
  return currentStory.value.current_player === currentUser.id;
});

const turnInfo = computed(() => {
  if (!currentStory.value || !roomStore.participants.length) return null;
  
  const currentPlayerParticipant = roomStore.participants.find(
    p => p.user === currentStory.value.current_player
  );
  
  return currentPlayerParticipant ? {
    username: currentPlayerParticipant.user_username,
    isMyTurn: isPlayerTurn.value
  } : null;
});

// Methods
const loadGameData = async () => {
  try {
    await Promise.all([
      roomStore.fetchRoom(roomId),
      roomStore.fetchParticipants(roomId),
      loadCurrentStory(),
      loadChapters()
    ]);
  } catch (error) {
    console.error('Error loading game data:', error);
  }
};

const loadCurrentStory = async () => {
  try {
    const response = await storytellingService.getCurrentStory(roomId);
    // Backend may return an object or an empty object; normalize
    currentStory.value = Array.isArray(response.data) ? response.data[0] : response.data;
    if (!currentStory.value || Object.keys(currentStory.value).length === 0) {
      currentStory.value = null;
      return;
    }
    await loadCurrentChapter();
  } catch (error) {
    console.error('Error loading current story:', error);
  }
};

const loadCurrentChapter = async () => {
  if (!currentStory.value?.current_chapter) return;
  
  try {
    const response = await storytellingService.getChapter(currentStory.value.current_chapter);
    currentChapter.value = response.data;
  } catch (error) {
    console.error('Error loading current chapter:', error);
  }
};

const loadChapters = async () => {
  if (!currentStory.value) return;
  
  try {
    const response = await storytellingService.getStoryChapters(currentStory.value.id);
    chapters.value = response.data.sort((a, b) => a.chapter_number - b.chapter_number);
  } catch (error) {
    console.error('Error loading chapters:', error);
  }
};

const submitPlayerAction = async () => {
  if (!playerAction.value.trim() || !isPlayerTurn.value) return;
  
  try {
    isSubmittingAction.value = true;
    
    // Submit player action
    await storytellingService.submitPlayerAction(roomId, {
      action_text: playerAction.value.trim(),
      chapter: currentChapter.value.id
    });
    
    // Clear action input
    playerAction.value = '';
    
    // Generate AI response
    await generateAIResponse();
    
    // Reload game state
    await loadGameData();
    
  } catch (error) {
    console.error('Error submitting action:', error);
  } finally {
    isSubmittingAction.value = false;
  }
};

// Typewriter animation for AI narrative
const typewriterRender = async (text) => {
  aiResponse.value = '';
  for (let i = 0; i < text.length; i++) {
    aiResponse.value += text[i];
    // slight acceleration on spaces/punctuation
    const ch = text[i];
    const delay = (ch === ' ' || ',.;:\n'.includes(ch)) ? 4 : 18;
    await new Promise(r => setTimeout(r, delay));
  }
  await nextTick();
  scrollToBottom();
};

const generateAIResponse = async () => {
  try {
    isGeneratingResponse.value = true;
    aiResponse.value = '';
    
    const response = await storytellingService.generateNarrative(roomId);
    const narrative = response.data?.narrative || '';
    await typewriterRender(narrative);
    
  } catch (error) {
    console.error('Error generating AI response:', error);
    aiResponse.value = 'Error generando respuesta de la IA. Int+峪talo nuevamente.';
  } finally {
    isGeneratingResponse.value = false;
  }
};

const sendChatMessage = () => {
  if (!newMessage.value.trim()) return;
  
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  chatMessages.value.push({
    id: Date.now(),
    user: user.username || 'Usuario',
    message: newMessage.value.trim(),
    timestamp: new Date().toLocaleTimeString()
  });
  
  newMessage.value = '';
  
  // Scroll to bottom of chat
  nextTick(() => {
    const chatContainer = document.getElementById('chat-messages');
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  });
};

const scrollToBottom = () => {
  const container = document.getElementById('narrative-content');
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
};

const leaveGame = () => {
  if (confirm('-+Est+疄 seguro de que quieres salir del juego?')) {
    router.push(`/rooms/${roomId}`);
  }
};

onMounted(async () => {
  if (!roomId) {
    router.push('/rooms');
    return;
  }

  // Ensure we have the latest room state before deciding
  try {
    await roomStore.fetchRoom(roomId);
  } catch {
    router.push('/rooms');
    return;
  }

  if (roomStore.currentRoom?.status !== 'playing') {
    router.push(`/rooms/${roomId}`);
    return;
  }

  await loadGameData();

  // If no story or no chapters yet, generate the first narrative
  if (!currentStory.value || !chapters.value || chapters.value.length === 0) {
    try {
      await generateAIResponse();
      await loadGameData();
  } catch {
      // ignore, UI will show error text
    }
  }
});
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 py-3">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-xl font-bold text-gray-800">{{ roomStore.currentRoom?.name }}</h1>
            <p class="text-sm text-gray-600">{{ currentStory?.title || 'Historia en Progreso' }}</p>
          </div>
          
          <!-- Turn indicator -->
          <div v-if="turnInfo" class="text-center">
            <div :class="['px-3 py-2 rounded-lg', turnInfo.isMyTurn ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800']">
              <p class="font-medium">
                {{ turnInfo.isMyTurn ? '-濭u Turno!' : `Turno de ${turnInfo.username}` }}
              </p>
            </div>
          </div>
          
          <button
            @click="leaveGame"
            class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm transition-colors"
          >
            Salir del Juego
          </button>
        </div>
      </div>
    </div>

    <!-- Main game area -->
    <div class="max-w-7xl mx-auto p-4 grid grid-cols-1 lg:grid-cols-4 gap-4 h-[calc(100vh-120px)]">
      
      <!-- Left sidebar: Participants and info -->
      <div class="lg:col-span-1 space-y-4">
        <!-- Participants -->
        <div class="bg-white rounded-lg shadow-md p-4">
          <h3 class="font-semibold mb-3">Jugadores</h3>
          <div class="space-y-2">
            <div
              v-for="participant in roomStore.participants"
              :key="participant.id"
              :class="[
                'p-2 rounded border',
                currentStory?.current_player === participant.user
                  ? 'bg-green-50 border-green-200'
                  : 'bg-gray-50 border-gray-200'
              ]"
            >
              <p class="font-medium text-sm">{{ participant.user_username }}</p>
              <p class="text-xs text-gray-600">
                {{ participant.character_names.join(', ') || 'Sin personajes' }}
              </p>
              <div v-if="currentStory?.current_player === participant.user" class="text-xs text-green-600 font-medium mt-1">
                Jugando...
              </div>
            </div>
          </div>
        </div>

        <!-- Story info -->
        <div class="bg-white rounded-lg shadow-md p-4">
          <h3 class="font-semibold mb-3">Historia</h3>
          <div class="text-sm space-y-2">
            <div>
              <span class="font-medium">Cap+﹀ulo:</span>
              <span class="ml-1">{{ currentChapter?.chapter_number || 0 }}</span>
            </div>
            <div>
              <span class="font-medium">Total Cap+﹀ulos:</span>
              <span class="ml-1">{{ chapters.length }}</span>
            </div>
            <div>
              <span class="font-medium">Universo:</span>
              <p class="text-gray-600">{{ roomStore.currentRoom?.universe_name }}</p>
            </div>
          </div>
        </div>

        <!-- Chat -->
        <div class="bg-white rounded-lg shadow-md p-4 flex flex-col h-64">
          <h3 class="font-semibold mb-3">Chat</h3>
          <div id="chat-messages" class="flex-1 overflow-y-auto space-y-2 mb-3">
            <div v-if="chatMessages.length === 0" class="text-gray-500 text-sm text-center py-4">
              No hay mensajes a+好
            </div>
            <div
              v-for="message in chatMessages"
              :key="message.id"
              class="text-sm"
            >
              <div class="flex items-center space-x-2">
                <span class="font-medium text-blue-600">{{ message.user }}:</span>
                <span class="text-xs text-gray-500">{{ message.timestamp }}</span>
              </div>
              <p class="text-gray-700 ml-2">{{ message.message }}</p>
            </div>
          </div>
          <div class="flex space-x-2">
            <input
              v-model="newMessage"
              @keyup.enter="sendChatMessage"
              type="text"
              placeholder="Escribe un mensaje..."
              class="flex-1 px-3 py-1 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              @click="sendChatMessage"
              class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm transition-colors"
            >
              Enviar
            </button>
          </div>
        </div>
      </div>

      <!-- Main narrative area -->
      <div class="lg:col-span-3">
        <div class="bg-white rounded-lg shadow-md h-full flex flex-col">
          <!-- Narrative content -->
          <div id="narrative-content" class="flex-1 p-6 overflow-y-auto">
            <h2 class="text-2xl font-bold mb-6 text-center text-gray-800">
              Cap+﹀ulo {{ currentChapter?.chapter_number || '' }}
            </h2>

            <!-- Chapter content -->
            <div v-if="currentChapter" class="prose max-w-none mb-6">
              <div class="bg-gray-50 p-4 rounded-lg mb-4">
                <h3 class="text-lg font-semibold mb-2">Narrativa del Cap+﹀ulo</h3>
                <p class="text-gray-700 leading-relaxed">{{ currentChapter.content }}</p>
              </div>
            </div>

            <!-- AI Response -->
            <div v-if="isGeneratingResponse || aiResponse" class="mb-6">
              <div class="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
                <h4 class="font-semibold text-blue-800 mb-2">Respuesta de la IA</h4>
                <div v-if="isGeneratingResponse" class="text-blue-600">
                  <div class="flex items-center space-x-2">
                    <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                    <span>Generando narrativa...</span>
                  </div>
                </div>
                <p v-else class="text-blue-700 leading-relaxed">{{ aiResponse }}</p>
              </div>
            </div>

            <!-- Chapter history -->
            <div v-if="chapters.length > 0" class="space-y-4">
              <h3 class="text-lg font-semibold">Historial de Cap+﹀ulos</h3>
              <div
                v-for="chapter in chapters"
                :key="chapter.id"
                :class="[
                  'p-4 rounded-lg border',
                  chapter.id === currentChapter?.id 
                    ? 'bg-yellow-50 border-yellow-200' 
                    : 'bg-gray-50 border-gray-200'
                ]"
              >
                <div class="flex justify-between items-start mb-2">
                  <h4 class="font-medium">Cap+﹀ulo {{ chapter.chapter_number }}</h4>
                  <span class="text-xs text-gray-500">{{ new Date(chapter.created_at).toLocaleDateString() }}</span>
                </div>
                <p class="text-gray-700 text-sm">{{ chapter.content }}</p>
              </div>
            </div>
          </div>

          <!-- Action input area -->
          <div class="border-t p-4">
            <div v-if="isPlayerTurn" class="space-y-3">
              <label class="block text-sm font-medium text-gray-700">
                Tu Acci+好
              </label>
              <textarea
                v-model="playerAction"
                :disabled="isSubmittingAction"
                placeholder="Describe la acci+好 que quiere realizar tu personaje..."
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
              ></textarea>
              <button
                @click="submitPlayerAction"
                :disabled="isSubmittingAction || !playerAction.trim()"
                class="bg-green-500 hover:bg-green-600 disabled:bg-green-300 text-white px-6 py-2 rounded-lg font-medium transition-colors"
              >
                {{ isSubmittingAction ? 'Enviando Acci+好...' : 'Enviar Acci+好' }}
              </button>
            </div>
            
            <div v-else class="text-center py-4">
              <p class="text-gray-600">
                {{ turnInfo ? `Esperando a ${turnInfo.username}...` : 'Esperando al siguiente jugador...' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.prose {
  max-width: none;
}

.prose p {
  margin-bottom: 1rem;
  line-height: 1.7;
}

.prose h3 {
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}
</style>
