<template>
  <div class="space-y-6">
    <div class="text-center mb-8">
      <h3 class="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
        Evaluaci+¦n por Inteligencia Artificial
      </h3>
      <p class="text-gray-400 mt-2">Nuestra IA analizar+í y mejorar+í tu personaje</p>
      <div class="mt-4 p-3 bg-yellow-900/20 border border-yellow-500/30 rounded-lg">
        <p class="text-yellow-400 text-sm flex items-center justify-center">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <strong>Paso Obligatorio:</strong> Debes evaluar tu personaje con IA y aceptar o rechazar las sugerencias para continuar
        </p>
      </div>
    </div>

    <!-- Estado inicial -->
    <div v-if="!hasRequestedEvaluation && !aiEvaluation" class="text-center py-12">
      <div class="w-24 h-24 mx-auto mb-6 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
        <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      </div>
      <h4 class="text-xl font-semibold text-white mb-4">-+Listo para la evaluaci+¦n IA?</h4>
      <p class="text-gray-400 mb-8 max-w-md mx-auto">
        Nuestra inteligencia artificial revisar+í tu personaje y sugerir+í mejoras creativas para hacerlo m+ís interesante y balanceado.
      </p>
      <button
        @click="$emit('request-ai-evaluation')"
        class="px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl font-semibold shadow-lg hover:from-purple-600 hover:to-pink-600 transform hover:scale-105 transition-all duration-300"
      >
        <span class="flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Solicitar Evaluaci+¦n IA
        </span>
      </button>
    </div>

    <!-- Cargando evaluaci+¦n -->
    <div v-else-if="isLoadingEvaluation" class="text-center py-12">
      <div class="w-24 h-24 mx-auto mb-6 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center animate-pulse">
        <div class="w-8 h-8 border-4 border-white border-t-transparent rounded-full animate-spin"></div>
      </div>
      <h4 class="text-xl font-semibold text-white mb-4">Analizando tu personaje...</h4>
      <p class="text-gray-400 mb-4">La IA est+í evaluando las caracter+¡sticas y generando sugerencias</p>
      <div class="w-full max-w-md mx-auto bg-gray-700 rounded-full h-2">
        <div class="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full animate-pulse" style="width: 60%"></div>
      </div>
    </div>

    <!-- Error en evaluaci+¦n -->
    <div v-else-if="evaluationError" class="text-center py-12">
      <div class="w-24 h-24 mx-auto mb-6 bg-red-500 rounded-full flex items-center justify-center">
        <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
      </div>
      <h4 class="text-xl font-semibold text-red-400 mb-4">Error en la evaluaci+¦n</h4>
      <div class="text-gray-400 mb-8 max-w-md mx-auto">
        <p class="text-red-300 font-medium mb-2">{{ evaluationError }}</p>
        <p class="text-sm">Por favor, verifica que todos los campos requeridos est+®n completos e intenta nuevamente.</p>
      </div>
      <div class="flex gap-4 justify-center">
        <button
          @click="$emit('request-ai-evaluation')"
          class="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-all duration-300"
        >
          Intentar de nuevo
        </button>
      </div>
    </div>

    <!-- Resultados de evaluaci+¦n -->
    <div v-else-if="aiEvaluation" class="space-y-6">
      <!-- Puntuaci+¦n general -->
      <div class="text-center p-6 bg-gradient-to-r from-purple-900/30 to-pink-900/30 rounded-xl border border-purple-500/20">
        <h4 class="text-2xl font-bold text-white mb-2">Puntuaci+¦n General</h4>
        <div class="text-6xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
          {{ aiEvaluation.overall_score || 'N/A' }}/10
        </div>
        <p class="text-gray-300">{{ getScoreDescription(aiEvaluation.overall_score) }}</p>
      </div>

      <!-- Mejoras sugeridas -->
      <div v-if="aiEvaluation.suggested_improvements" class="space-y-4">
        <h4 class="text-lg font-semibold text-purple-400 flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Mejoras Sugeridas por IA
        </h4>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Fortalezas mejoradas -->
          <div v-if="aiEvaluation.suggested_improvements.strengths" class="space-y-3">
            <h5 class="font-medium text-emerald-400 flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Fortalezas Sugeridas
            </h5>
            <div class="p-4 bg-emerald-900/20 border border-emerald-500/20 rounded-lg">
              <p class="text-gray-300 text-sm whitespace-pre-line">{{ aiEvaluation.suggested_improvements.strengths }}</p>
            </div>
          </div>

          <!-- Debilidades mejoradas -->
          <div v-if="aiEvaluation.suggested_improvements.weaknesses" class="space-y-3">
            <h5 class="font-medium text-red-400 flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              Debilidades Sugeridas
            </h5>
            <div class="p-4 bg-red-900/20 border border-red-500/20 rounded-lg">
              <p class="text-gray-300 text-sm whitespace-pre-line">{{ aiEvaluation.suggested_improvements.weaknesses }}</p>
            </div>
          </div>

          <!-- Historia mejorada -->
          <div v-if="aiEvaluation.suggested_improvements.history" class="md:col-span-2 space-y-3">
            <h5 class="font-medium text-blue-400 flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              Historia/Trasfondo Sugerido
            </h5>
            <div class="p-4 bg-blue-900/20 border border-blue-500/20 rounded-lg">
              <p class="text-gray-300 text-sm whitespace-pre-line">{{ aiEvaluation.suggested_improvements.history }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Comentarios de la IA -->
      <div v-if="aiEvaluation.comments" class="space-y-3">
        <h4 class="text-lg font-semibold text-purple-400 flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          Comentarios de la IA
        </h4>
        <div class="p-4 bg-purple-900/20 border border-purple-500/20 rounded-lg">
          <p class="text-gray-300 text-sm whitespace-pre-line">{{ aiEvaluation.comments }}</p>
        </div>
      </div>

      <!-- Botones de acci+¦n -->
      <div class="flex flex-col sm:flex-row gap-4 pt-6 border-t border-gray-700/50">
        <button
          @click="$emit('accept-ai-suggestions')"
          class="flex-1 flex items-center justify-center px-6 py-3 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg font-medium hover:from-emerald-600 hover:to-blue-600 transition-all duration-300 transform hover:scale-105"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Aceptar y Continuar
        </button>
        <button
          @click="$emit('reject-ai-suggestions')"
          class="flex-1 flex items-center justify-center px-6 py-3 bg-orange-600 text-white rounded-lg font-medium hover:bg-orange-700 transition-all duration-300"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 17l-5-5m0 0l5-5m-5 5h12" />
          </svg>
          Rechazar y Modificar
        </button>
        <button
          @click="$emit('request-ai-evaluation')"
          class="flex items-center justify-center px-6 py-3 bg-purple-600 text-white rounded-lg font-medium hover:bg-purple-700 transition-all duration-300"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Nueva Evaluaci+¦n
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  hasRequestedEvaluation: {
    type: Boolean,
    default: false
  },
  isLoadingEvaluation: {
    type: Boolean,
    default: false
  },
  aiEvaluation: {
    type: Object,
    default: null
  },
  evaluationError: {
    type: String,
    default: null
  }
});

defineEmits([
  'request-ai-evaluation',
  'accept-ai-suggestions', 
  'reject-ai-suggestions'
]);

const getScoreDescription = (score) => {
  if (!score) return 'Sin evaluaci+¦n';
  if (score >= 9) return 'Excelente personaje';
  if (score >= 8) return 'Muy buen personaje';
  if (score >= 7) return 'Buen personaje';
  if (score >= 6) return 'Personaje decente';
  if (score >= 5) return 'Personaje promedio';
  return 'Necesita mejoras';
};
</script>
