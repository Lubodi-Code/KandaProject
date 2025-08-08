<template>
  <div class="flex justify-between items-center pt-6 border-t border-gray-700/50">
    <!-- Bot+好 Anterior -->
    <button
      v-if="showPrevious"
      @click="$emit('previous')"
      :disabled="isPreviousDisabled"
      :class="[
        'flex items-center px-6 py-3 rounded-lg font-medium transition-all duration-300 shadow-lg transform',
        isPreviousDisabled
          ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
          : 'bg-gray-600 hover:bg-gray-500 text-white hover:scale-105 hover:shadow-xl'
      ]"
    >
      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
      Anterior
    </button>
    <div v-else></div>

    <!-- Botones de acci+好 central (opcionales) -->
    <div v-if="$slots.center" class="flex space-x-3">
      <slot name="center"></slot>
    </div>

    <!-- Bot+好 Siguiente/Finalizar -->
    <button
      @click="$emit(isLastStep ? 'submit' : 'next')"
      :disabled="isNextDisabled"
      :class="[
        'flex items-center px-6 py-3 rounded-lg font-medium transition-all duration-300 shadow-lg transform relative overflow-hidden',
        isNextDisabled
          ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
          : isLastStep
            ? 'bg-gradient-to-r from-emerald-500 to-blue-500 hover:from-emerald-600 hover:to-blue-600 text-white hover:scale-105 hover:shadow-2xl'
            : 'bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white hover:scale-105 hover:shadow-xl'
      ]"
    >
      <span class="relative z-10 flex items-center">
        {{ isLastStep ? finalButtonText : nextButtonText }}
        <svg v-if="!isLastStep" class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
        <svg v-else class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
      </span>
      
      <!-- Efecto de brillo para el bot+好 final -->
      <div 
        v-if="isLastStep && !isNextDisabled" 
        class="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-20 transform -skew-x-12 animate-shine"
      ></div>
    </button>
  </div>
</template>

<script setup>
defineProps({
  showPrevious: {
    type: Boolean,
    default: true
  },
  isPreviousDisabled: {
    type: Boolean,
    default: false
  },
  isNextDisabled: {
    type: Boolean,
    default: false
  },
  isLastStep: {
    type: Boolean,
    default: false
  },
  nextButtonText: {
    type: String,
    default: 'Siguiente'
  },
  finalButtonText: {
    type: String,
    default: 'Crear Personaje'
  }
});

defineEmits(['previous', 'next', 'submit']);
</script>

<style scoped>
@keyframes shine {
  0% {
    transform: translateX(-100%) skewX(-12deg);
  }
  100% {
    transform: translateX(200%) skewX(-12deg);
  }
}

.animate-shine {
  animation: shine 2s ease-in-out infinite;
}
</style>
