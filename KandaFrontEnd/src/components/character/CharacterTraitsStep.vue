<template>
  <div class="space-y-6">
    <div class="text-center mb-8">
      <h3 class="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-blue-400 bg-clip-text text-transparent">
        Caracter+¡sticas del Personaje
      </h3>
      <p class="text-gray-400 mt-2">Define la personalidad y trasfondo de tu personaje</p>
    </div>

    <!-- Personalidad -->
    <div class="space-y-2">
      <label class="text-sm font-medium text-gray-300 flex items-center">
        <svg class="w-4 h-4 mr-2 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
        Personalidad *
      </label>
      <textarea
        v-model="form.personality"
        required
        rows="4"
        placeholder="Describe la personalidad de tu personaje: es extrovertido, t+¡mido, aventurero, cauteloso, optimista, etc..."
        :class="[inputClasses, 'resize-none']"
        @blur="validateField('personality')"
      ></textarea>
      <p v-if="errors.personality" class="text-red-400 text-xs mt-1">{{ errors.personality }}</p>
      <div class="flex justify-between text-xs text-gray-500">
        <span>M+¡nimo 10 caracteres</span>
        <span>{{ form.personality?.length || 0 }}/800</span>
      </div>
    </div>

    <!-- Historia -->
    <div class="space-y-2">
      <div class="flex items-center justify-between">
        <label class="text-sm font-medium text-gray-300 flex items-center">
          <svg class="w-4 h-4 mr-2 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          Historia/Trasfondo
        </label>
        <button
          v-if="!form.history || form.history.length < 50"
          @click="$emit('generate-background')"
          :disabled="isGeneratingBackground"
          class="flex items-center px-3 py-1 text-xs bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all duration-300 disabled:opacity-50"
        >
          <svg v-if="!isGeneratingBackground" class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <div v-else class="w-3 h-3 border border-white border-t-transparent rounded-full animate-spin mr-1"></div>
          {{ isGeneratingBackground ? 'Generando...' : 'Generar con IA' }}
        </button>
      </div>
      <textarea
        v-model="form.history"
        rows="5"
        placeholder="Cuenta la historia de tu personaje: de d+¦nde viene, experiencias importantes, familia, eventos que lo marcaron... (Opcional - puede ser generado por IA)"
        :class="[inputClasses, 'resize-none']"
      ></textarea>
      <div class="flex justify-between text-xs text-gray-500">
        <span>Campo opcional</span>
        <span>{{ form.history?.length || 0 }}/1200</span>
      </div>
    </div>

    <!-- Fortalezas y Debilidades -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Fortalezas -->
      <div class="space-y-2">
        <label class="text-sm font-medium text-gray-300 flex items-center">
          <svg class="w-4 h-4 mr-2 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Fortalezas *
        </label>
        <textarea
          v-model="form.strengths"
          required
          rows="3"
          placeholder="Ej: Valiente, leal, inteligente, carism+ítico..."
          :class="[inputClasses, 'resize-none']"
          @blur="validateField('strengths')"
        ></textarea>
        <p v-if="errors.strengths" class="text-red-400 text-xs mt-1">{{ errors.strengths }}</p>
        <div class="text-xs text-gray-500 text-right">
          {{ form.strengths?.length || 0 }}/400
        </div>
      </div>

      <!-- Debilidades -->
      <div class="space-y-2">
        <label class="text-sm font-medium text-gray-300 flex items-center">
          <svg class="w-4 h-4 mr-2 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          Debilidades *
        </label>
        <textarea
          v-model="form.weaknesses"
          required
          rows="3"
          placeholder="Ej: Impulsivo, orgulloso, desconfiado, temeroso..."
          :class="[inputClasses, 'resize-none']"
          @blur="validateField('weaknesses')"
        ></textarea>
        <p v-if="errors.weaknesses" class="text-red-400 text-xs mt-1">{{ errors.weaknesses }}</p>
        <div class="text-xs text-gray-500 text-right">
          {{ form.weaknesses?.length || 0 }}/400
        </div>
      </div>
    </div>

    <!-- Habilidades Especiales -->
    <div class="space-y-2">
      <label class="text-sm font-medium text-gray-300 flex items-center">
        <svg class="w-4 h-4 mr-2 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
        </svg>
        Habilidades Especiales
      </label>
      <textarea
        v-model="form.special_abilities"
        rows="3"
        placeholder="Describe habilidades +¦nicas, talentos especiales, poderes, conocimientos espec+¡ficos... (Opcional)"
        :class="[inputClasses, 'resize-none']"
      ></textarea>
      <div class="text-xs text-gray-500 text-right">
        {{ form.special_abilities?.length || 0 }}/600
      </div>
    </div>

    <!-- Objetivos -->
    <div class="space-y-2">
      <label class="text-sm font-medium text-gray-300 flex items-center">
        <svg class="w-4 h-4 mr-2 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
        </svg>
        Objetivos/Motivaciones
      </label>
      <textarea
        v-model="form.goals"
        rows="3"
        placeholder="-+Qu+® busca tu personaje? -+Cu+íles son sus motivaciones principales? (Opcional)"
        :class="[inputClasses, 'resize-none']"
      ></textarea>
      <div class="text-xs text-gray-500 text-right">
        {{ form.goals?.length || 0 }}/500
      </div>
    </div>

    <!-- Resumen de Caracter+¡sticas -->
    <div v-if="isFormValid" class="mt-8 p-6 bg-gradient-to-r from-emerald-900/20 to-blue-900/20 rounded-xl border border-emerald-500/20">
      <h4 class="text-lg font-semibold text-emerald-400 mb-4 flex items-center">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        Caracter+¡sticas Definidas
      </h4>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="space-y-2">
          <div>
            <span class="text-gray-400 text-sm">Personalidad:</span>
            <p class="text-white text-sm">{{ truncateText(form.personality, 100) }}</p>
          </div>
          <div v-if="form.history">
            <span class="text-gray-400 text-sm">Historia:</span>
            <p class="text-white text-sm">{{ truncateText(form.history, 100) }}</p>
          </div>
        </div>
        <div class="space-y-2">
          <div>
            <span class="text-gray-400 text-sm">Fortalezas:</span>
            <p class="text-white text-sm">{{ truncateText(form.strengths, 80) }}</p>
          </div>
          <div>
            <span class="text-gray-400 text-sm">Debilidades:</span>
            <p class="text-white text-sm">{{ truncateText(form.weaknesses, 80) }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive } from 'vue';

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  isGeneratingBackground: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue', 'validation-change', 'generate-background']);

const form = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const errors = reactive({});

const inputClasses = `
  w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white 
  placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 
  focus:border-transparent transition-all duration-300 hover:border-gray-500
`;

const validateField = (field) => {
  switch (field) {
    case 'personality':
      if (!form.value.personality || form.value.personality.trim().length < 10) {
        errors[field] = 'La personalidad debe tener al menos 10 caracteres';
      } else if (form.value.personality.length > 800) {
        errors[field] = 'La personalidad no debe exceder 800 caracteres';
      } else {
        delete errors[field];
      }
      break;
    case 'strengths':
      if (!form.value.strengths || form.value.strengths.trim().length < 5) {
        errors[field] = 'Las fortalezas deben tener al menos 5 caracteres';
      } else if (form.value.strengths.length > 400) {
        errors[field] = 'Las fortalezas no deben exceder 400 caracteres';
      } else {
        delete errors[field];
      }
      break;
    case 'weaknesses':
      if (!form.value.weaknesses || form.value.weaknesses.trim().length < 5) {
        errors[field] = 'Las debilidades deben tener al menos 5 caracteres';
      } else if (form.value.weaknesses.length > 400) {
        errors[field] = 'Las debilidades no deben exceder 400 caracteres';
      } else {
        delete errors[field];
      }
      break;
  }
  
  emit('validation-change', isFormValid.value);
};

const isFormValid = computed(() => {
  return form.value.personality?.trim().length >= 10 &&
         form.value.strengths?.trim().length >= 5 &&
         form.value.weaknesses?.trim().length >= 5 &&
         Object.keys(errors).length === 0;
});

const truncateText = (text, maxLength) => {
  if (!text) return '';
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
};

// Watchers para validaci+¦n en tiempo real
import { watch } from 'vue';

watch(() => form.value.personality, () => validateField('personality'));
watch(() => form.value.strengths, () => validateField('strengths'));
watch(() => form.value.weaknesses, () => validateField('weaknesses'));
</script>
