<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { characterService } from '../api/characters';
import { useRoomStore } from '../stores/storytelling';
import CharacterFormModal from '../components/CharacterFormModal.vue';

const router = useRouter();
const roomStore = useRoomStore();

const characters = ref([]);
const showModal = ref(false);
const editingCharacter = ref(null);
const activeTab = ref('characters');

const fetchCharacters = async () => {
  const res = await characterService.list();
  characters.value = res.data;
};

const openCreate = () => {
  editingCharacter.value = null;
  showModal.value = true;
};

const openEdit = character => {
  editingCharacter.value = { ...character };
  showModal.value = true;
};

const saveCharacter = async data => {
  if (editingCharacter.value && editingCharacter.value.id) {
    await characterService.update(editingCharacter.value.id, data);
  } else {
    // TEMPORAL: Usar endpoint de testing para nuevos personajes
    await characterService.createCharacterTest(data);
  }
  showModal.value = false;
  await fetchCharacters();
};

const deleteCharacter = async id => {
  await characterService.delete(id);
  await fetchCharacters();
};

const createDefault = async () => {
  await characterService.createDefault();
  await fetchCharacters();
};

onMounted(fetchCharacters);
</script>

<template>
  <div class="p-4">
    <div class="mb-4 space-x-2">
      <button @click="openCreate" class="px-3 py-1 bg-green-500 text-white">Crear Nuevo Personaje</button>
      <button @click="createDefault" class="px-3 py-1 bg-indigo-500 text-white">Crear Personaje Por Defecto</button>
    </div>

    <div v-if="characters.length === 0">No hay personajes.</div>
    <div v-else class="space-y-2">
      <div v-for="c in characters" :key="c.id" class="border p-2 rounded">
        <h3 class="font-bold">{{ c.name }}</h3>
        <p>{{ c.archetype }} - {{ c.gender }}</p>
        <p><strong>Físico:</strong> {{ (c.physical_traits || []).join(', ') }}</p>
        <p><strong>Personalidad:</strong> {{ (c.personality_traits || []).join(', ') }}</p>
        <p><strong>Historia:</strong> {{ c.background }}</p>
        <p><strong>Fortalezas:</strong> {{ (c.aiFilter?.strengths || []).join(', ') }}</p>
        <p><strong>Debilidades:</strong> {{ (c.aiFilter?.flaws || []).join(', ') }}</p>
        <div class="space-x-2 mt-2">
          <button @click="openEdit(c)" class="px-2 py-1 bg-yellow-500 text-white">Editar</button>
          <button @click="deleteCharacter(c.id)" class="px-2 py-1 bg-red-500 text-white">Eliminar</button>
        </div>
      </div>
    </div>

    <CharacterFormModal
      v-if="showModal"
      :character="editingCharacter"
      @close="showModal = false"
      @character-saved="saveCharacter"
    />
  </div>
</template>
