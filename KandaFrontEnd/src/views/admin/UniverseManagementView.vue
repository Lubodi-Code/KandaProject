<script setup>
import { ref, onMounted, computed } from 'vue';
import { useUniverseStore } from '../../stores/storytelling';

const universeStore = useUniverseStore();

const showCreateModal = ref(false);
const editingUniverse = ref(null);
const loading = ref(false);

// Form data
const formData = ref({
  name: '',
  description: '',
  setting: '',
  rules: '',
  tone: '',
  themes: ''
});

// Computed
const isEditing = computed(() => !!editingUniverse.value);

// Methods
const loadUniverses = async () => {
  try {
    loading.value = true;
    await universeStore.fetchUniverses();
  } catch (error) {
    console.error('Error loading universes:', error);
  } finally {
    loading.value = false;
  }
};

const openCreateModal = () => {
  editingUniverse.value = null;
  formData.value = {
    name: '',
    description: '',
    setting: '',
    rules: '',
    tone: '',
    themes: ''
  };
  showCreateModal.value = true;
};

const openEditModal = (universe) => {
  editingUniverse.value = universe;
  formData.value = {
    name: universe.name || '',
    description: universe.description || '',
    setting: universe.setting || '',
    rules: universe.rules || '',
    tone: universe.tone || '',
    themes: universe.themes || ''
  };
  showCreateModal.value = true;
};

const closeModal = () => {
  showCreateModal.value = false;
  editingUniverse.value = null;
  formData.value = {
    name: '',
    description: '',
    setting: '',
    rules: '',
    tone: '',
    themes: ''
  };
};

const saveUniverse = async () => {
  try {
    loading.value = true;
    
    if (isEditing.value) {
      await universeStore.updateUniverse(editingUniverse.value.id, formData.value);
    } else {
      await universeStore.createUniverse(formData.value);
    }
    
    closeModal();
    await loadUniverses();
  } catch (error) {
    console.error('Error saving universe:', error);
  } finally {
    loading.value = false;
  }
};

const deleteUniverse = async (universe) => {
  if (!confirm(`-+Est+ís seguro de que quieres eliminar el universo "${universe.name}"? Esta acci+¦n no se puede deshacer.`)) {
    return;
  }
  
  try {
    loading.value = true;
    await universeStore.deleteUniverse(universe.id);
    await loadUniverses();
  } catch (error) {
    console.error('Error deleting universe:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadUniverses();
});
</script>

<template>
  <div class="p-4 max-w-7xl mx-auto">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-3xl font-bold text-gray-800">Administrar Universos</h1>
        <p class="text-gray-600 mt-1">Crea y gestiona los universos narrativos para las historias</p>
      </div>
      <button
        @click="openCreateModal"
        class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg font-medium transition-colors"
      >
        Crear Nuevo Universo
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="loading && universeStore.universes.length === 0" class="text-center py-8">
      <p class="text-gray-500">Cargando universos...</p>
    </div>

    <!-- Universes grid -->
    <div v-else-if="universeStore.universes.length > 0" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="universe in universeStore.universes"
        :key="universe.id"
        class="bg-white rounded-lg shadow-md overflow-hidden"
      >
        <div class="p-6">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xl font-semibold text-gray-800">{{ universe.name }}</h3>
            <div class="flex space-x-2">
              <button
                @click="openEditModal(universe)"
                class="text-blue-500 hover:text-blue-700 text-sm font-medium"
              >
                Editar
              </button>
              <button
                @click="deleteUniverse(universe)"
                class="text-red-500 hover:text-red-700 text-sm font-medium"
              >
                Eliminar
              </button>
            </div>
          </div>
          
          <p class="text-gray-600 mb-4 line-clamp-3">{{ universe.description || 'Sin descripci+¦n' }}</p>
          
          <div class="space-y-2 text-sm">
            <div v-if="universe.setting">
              <span class="font-medium text-gray-700">Ambientaci+¦n:</span>
              <p class="text-gray-600 mt-1">{{ universe.setting }}</p>
            </div>
            
            <div v-if="universe.tone">
              <span class="font-medium text-gray-700">Tono:</span>
              <span class="ml-2 px-2 py-1 bg-gray-100 rounded text-xs">{{ universe.tone }}</span>
            </div>
            
            <div v-if="universe.themes">
              <span class="font-medium text-gray-700">Temas:</span>
              <p class="text-gray-600 mt-1">{{ universe.themes }}</p>
            </div>
          </div>
          
          <div class="mt-4 pt-4 border-t text-xs text-gray-500">
            Creado: {{ new Date(universe.created_at).toLocaleDateString() }}
          </div>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else class="text-center py-12">
      <div class="max-w-md mx-auto">
        <h3 class="text-lg font-medium text-gray-800 mb-2">No hay universos creados</h3>
        <p class="text-gray-600 mb-6">Comienza creando tu primer universo narrativo para las historias</p>
        <button
          @click="openCreateModal"
          class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg font-medium transition-colors"
        >
          Crear Primer Universo
        </button>
      </div>
    </div>

    <!-- Error state -->
    <div v-if="universeStore.error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
      <p>{{ universeStore.error }}</p>
      <button
        @click="universeStore.clearError(); loadUniverses()"
        class="mt-2 text-sm underline"
      >
        Reintentar
      </button>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-800">
              {{ isEditing ? 'Editar Universo' : 'Crear Nuevo Universo' }}
            </h2>
            <button
              @click="closeModal"
              class="text-gray-500 hover:text-gray-700 text-2xl"
            >
              +ù
            </button>
          </div>

          <form @submit.prevent="saveUniverse" class="space-y-4">
            <!-- Name -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Nombre del Universo *
              </label>
              <input
                v-model="formData.name"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Ej: Mundo Fant+ístico Medieval"
              />
            </div>

            <!-- Description -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Descripci+¦n
              </label>
              <textarea
                v-model="formData.description"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Describe este universo y sus caracter+¡sticas principales"
              ></textarea>
            </div>

            <!-- Setting -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Ambientaci+¦n
              </label>
              <textarea
                v-model="formData.setting"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Describe el mundo, +®poca, lugares importantes, cultura, etc."
              ></textarea>
            </div>

            <!-- Rules -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Reglas del Mundo
              </label>
              <textarea
                v-model="formData.rules"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Leyes f+¡sicas, magia, tecnolog+¡a, reglas sociales, etc."
              ></textarea>
            </div>

            <!-- Tone -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Tono Narrativo
              </label>
              <select
                v-model="formData.tone"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Seleccionar tono...</option>
                <option value="+®pico">+ëpico</option>
                <option value="dram+ítico">Dram+ítico</option>
                <option value="humor+¡stico">Humor+¡stico</option>
                <option value="misterioso">Misterioso</option>
                <option value="rom+íntico">Rom+íntico</option>
                <option value="terror">Terror</option>
                <option value="aventura">Aventura</option>
                <option value="melanc+¦lico">Melanc+¦lico</option>
              </select>
            </div>

            <!-- Themes -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Temas Principales
              </label>
              <textarea
                v-model="formData.themes"
                rows="2"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Honor, venganza, amor, poder, supervivencia, etc."
              ></textarea>
            </div>

            <!-- Action buttons -->
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeModal"
                class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg transition-colors"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="loading || !formData.name.trim()"
                class="bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white px-6 py-2 rounded-lg font-medium transition-colors"
              >
                {{ loading ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Crear Universo') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
