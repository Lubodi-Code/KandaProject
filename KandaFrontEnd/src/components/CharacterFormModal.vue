<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  character: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['close', 'character-saved']);

const form = ref({
  name: '',
  archetype: '',
  gender: '',
  background: ''
});
const physicalTraitsInput = ref('');
const personalityTraitsInput = ref('');
const aiStrengths = ref([]);
const aiFlaws = ref([]);

watch(
  () => props.character,
  newVal => {
    if (newVal) {
      form.value = {
        name: newVal.name || '',
        archetype: newVal.archetype || '',
        gender: newVal.gender || '',
        background: newVal.background || ''
      };
      physicalTraitsInput.value = (newVal.physical_traits || []).join(', ');
      personalityTraitsInput.value = (newVal.personality_traits || []).join(', ');
      aiStrengths.value = newVal.aiFilter?.strengths || [];
      aiFlaws.value = newVal.aiFilter?.flaws || [];
    } else {
      form.value = { name: '', archetype: '', gender: '', background: '' };
      physicalTraitsInput.value = '';
      personalityTraitsInput.value = '';
      aiStrengths.value = [];
      aiFlaws.value = [];
    }
  },
  { immediate: true }
);

const save = () => {
  const payload = {
    name: form.value.name,
    archetype: form.value.archetype,
    gender: form.value.gender,
    physical_traits: physicalTraitsInput.value.split(',').map(s => s.trim()).filter(Boolean),
    personality_traits: personalityTraitsInput.value.split(',').map(s => s.trim()).filter(Boolean),
    background: form.value.background
  };
  emit('character-saved', payload);
};
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white p-4 rounded w-96">
      <h2 class="text-lg font-bold mb-4">
        {{ props.character ? 'Editar Personaje' : 'Nuevo Personaje' }}
      </h2>
      <div class="space-y-2">
        <label class="block">
          Nombre
          <input v-model="form.name" type="text" class="w-full border p-1" />
        </label>
        <label class="block">
          Arquetipo
          <input v-model="form.archetype" type="text" class="w-full border p-1" />
        </label>
        <label class="block">
          Género
          <input v-model="form.gender" type="text" class="w-full border p-1" />
        </label>
        <label class="block">
          Aspectos Físicos
          <input v-model="physicalTraitsInput" type="text" placeholder="Separados por comas" class="w-full border p-1" />
        </label>
        <label class="block">
          Aspectos de Personalidad
          <input v-model="personalityTraitsInput" type="text" placeholder="Separadas por comas" class="w-full border p-1" />
        </label>
        <label class="block">
          Historia o Antecedentes
          <textarea v-model="form.background" class="w-full border p-1"></textarea>
        </label>
        <div v-if="aiStrengths.length || aiFlaws.length" class="mt-2">
          <p><strong>Fortalezas sugeridas:</strong> {{ aiStrengths.join(', ') }}</p>
          <p><strong>Debilidades sugeridas:</strong> {{ aiFlaws.join(', ') }}</p>
        </div>
      </div>
      <div class="mt-4 flex justify-end space-x-2">
        <button @click="$emit('close')" class="px-3 py-1 border">Cancelar</button>
        <button @click="save" class="px-3 py-1 bg-blue-500 text-white">Guardar</button>
      </div>
    </div>
  </div>
</template>
