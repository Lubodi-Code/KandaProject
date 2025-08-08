<template>
  <div class="space-y-6">
    <div class="text-center mb-8">
      <h3 class="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-blue-400 bg-clip-text text-transparent">
        Confirmar Creaci+¦n
      </h3>
      <p class="text-gray-400 mt-2">Revisa todos los detalles antes de crear tu personaje</p>
    </div>

    <!-- Resumen del personaje -->
    <div class="space-y-6">
      <!-- Informaci+¦n b+ísica -->
      <div class="p-6 bg-gradient-to-r from-gray-800/50 to-gray-900/50 rounded-xl border border-gray-700/50">
        <h4 class="text-lg font-semibold text-emerald-400 mb-4 flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          Informaci+¦n B+ísica
        </h4>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <span class="text-gray-400 text-sm">Nombre:</span>
            <p class="text-white font-medium">{{ characterData.name }}</p>
          </div>
          <div>
            <span class="text-gray-400 text-sm">Edad:</span>
            <p class="text-white font-medium">{{ characterData.age }} a+¦os</p>
          </div>
          <div>
            <span class="text-gray-400 text-sm">G+®nero:</span>
            <p class="text-white font-medium">{{ characterData.gender }}</p>
          </div>
          <div v-if="characterData.nationality">
            <span class="text-gray-400 text-sm">Nacionalidad:</span>
            <p class="text-white font-medium">{{ characterData.nationality }}</p>
          </div>
        </div>
        <div v-if="characterData.physical_description" class="mt-4">
          <span class="text-gray-400 text-sm">Descripci+¦n F+¡sica:</span>
          <p class="text-white text-sm mt-1">{{ characterData.physical_description }}</p>
        </div>
      </div>

      <!-- Caracter+¡sticas -->
      <div class="p-6 bg-gradient-to-r from-gray-800/50 to-gray-900/50 rounded-xl border border-gray-700/50">
        <h4 class="text-lg font-semibold text-blue-400 mb-4 flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          Caracter+¡sticas
        </h4>
        <div class="space-y-4">
          <div v-if="characterData.personality">
            <span class="text-gray-400 text-sm">Personalidad:</span>
            <p class="text-white text-sm mt-1">{{ characterData.personality }}</p>
          </div>
          <div v-if="characterData.history" class="grid grid-cols-1 md:grid-cols-1 gap-4">
            <div>
              <span class="text-gray-400 text-sm">Historia/Trasfondo:</span>
              <p class="text-white text-sm mt-1">{{ characterData.history }}</p>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-if="characterData.strengths">
              <span class="text-emerald-400 text-sm">Fortalezas:</span>
              <p class="text-white text-sm mt-1">{{ characterData.strengths }}</p>
            </div>
            <div v-if="characterData.weaknesses">
              <span class="text-red-400 text-sm">Debilidades:</span>
              <p class="text-white text-sm mt-1">{{ characterData.weaknesses }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Informaci+¦n adicional -->
      <div v-if="characterData.special_abilities || characterData.goals" class="p-6 bg-gradient-to-r from-gray-800/50 to-gray-900/50 rounded-xl border border-gray-700/50">
        <h4 class="text-lg font-semibold text-purple-400 mb-4 flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
          </svg>
          Informaci+¦n Adicional
        </h4>
        <div class="space-y-4">
          <div v-if="characterData.special_abilities">
            <span class="text-gray-400 text-sm">Habilidades Especiales:</span>
            <p class="text-white text-sm mt-1">{{ characterData.special_abilities }}</p>
          </div>
          <div v-if="characterData.goals">
            <span class="text-gray-400 text-sm">Objetivos/Motivaciones:</span>
            <p class="text-white text-sm mt-1">{{ characterData.goals }}</p>
          </div>
        </div>
      </div>

      <!-- Evaluaci+¦n IA (si existe) -->
      <div v-if="aiEvaluation" class="p-6 bg-gradient-to-r from-purple-900/30 to-pink-900/30 rounded-xl border border-purple-500/20">
        <h4 class="text-lg font-semibold text-purple-400 mb-4 flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Evaluaci+¦n por IA
        </h4>
        <div class="flex items-center justify-between mb-4">
          <span class="text-gray-300">Puntuaci+¦n General:</span>
          <div class="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            {{ aiEvaluation.overall_score }}/10
          </div>
        </div>
        <div v-if="aiEvaluation.comments" class="mt-4">
          <span class="text-gray-400 text-sm">Comentarios de la IA:</span>
          <p class="text-white text-sm mt-1">{{ aiEvaluation.comments }}</p>
        </div>
      </div>

      <!-- Advertencias o validaciones -->
      <div v-if="validationWarnings.length > 0" class="p-4 bg-yellow-900/20 border border-yellow-500/20 rounded-lg">
        <h5 class="text-yellow-400 font-medium mb-2 flex items-center">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          Advertencias
        </h5>
        <ul class="text-yellow-300 text-sm space-y-1">
          <li v-for="warning in validationWarnings" :key="warning">ÔÇó {{ warning }}</li>
        </ul>
      </div>

      <!-- Estado de carga -->
      <div v-if="isCreating" class="text-center py-8">
        <div class="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-emerald-500 to-blue-500 rounded-full flex items-center justify-center">
          <div class="w-8 h-8 border-4 border-white border-t-transparent rounded-full animate-spin"></div>
        </div>
        <h4 class="text-lg font-semibold text-white mb-2">Creando personaje...</h4>
        <p class="text-gray-400">Guardando toda la informaci+¦n</p>
      </div>

      <!-- Confirmaci+¦n final -->
      <div v-if="!isCreating" class="p-6 bg-gradient-to-r from-emerald-900/20 to-blue-900/20 rounded-xl border border-emerald-500/20">
        <div class="flex items-start space-x-3">
          <div class="flex-shrink-0">
            <svg class="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h5 class="text-emerald-400 font-medium mb-2">-+Listo para crear tu personaje?</h5>
            <p class="text-gray-300 text-sm mb-4">
              Una vez creado, podr+ís editarlo desde tu dashboard. Aseg+¦rate de que toda la informaci+¦n sea correcta.
            </p>
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>El personaje se guardar+í en tu colecci+¦n personal</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  characterData: {
    type: Object,
    required: true
  },
  aiEvaluation: {
    type: Object,
    default: null
  },
  isCreating: {
    type: Boolean,
    default: false
  }
});

const validationWarnings = computed(() => {
  const warnings = [];
  
  if (!props.characterData.history || props.characterData.history.length < 50) {
    warnings.push('El personaje no tiene una historia detallada');
  }
  
  if (!props.characterData.special_abilities) {
    warnings.push('No se han definido habilidades especiales');
  }
  
  if (!props.characterData.goals) {
    warnings.push('No se han definido objetivos o motivaciones');
  }
  
  if (!props.aiEvaluation) {
    warnings.push('El personaje no ha sido evaluado por IA');
  } else if (props.aiEvaluation.overall_score < 6) {
    warnings.push('La evaluaci+¦n IA indica que el personaje podr+¡a mejorarse');
  }
  
  return warnings;
});
</script>
