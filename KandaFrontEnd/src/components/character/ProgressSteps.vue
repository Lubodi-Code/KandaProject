<template>
  <div class="relative">
    <div class="flex justify-between items-center mb-2">
      <div 
        v-for="step in totalSteps" 
        :key="step"
        @click="$emit('goToStep', step)"
        :class="[
          'flex items-center justify-center w-12 h-12 rounded-full cursor-pointer transition-all duration-300 text-sm font-bold relative',
          currentStep >= step 
            ? 'bg-gradient-to-r from-emerald-400 to-blue-400 text-white shadow-lg scale-110' 
            : 'bg-gray-700 text-gray-400 hover:bg-gray-600 hover:scale-105'
        ]"
      >
        <span class="relative z-10">{{ step }}</span>
        <div 
          v-if="currentStep >= step" 
          class="absolute inset-0 rounded-full bg-gradient-to-r from-emerald-400 to-blue-400 animate-pulse opacity-20"
        ></div>
      </div>
    </div>
    
    <!-- Barra de progreso -->
    <div class="h-3 bg-gray-700 rounded-full overflow-hidden relative">
      <div 
        class="h-full bg-gradient-to-r from-emerald-400 to-blue-400 rounded-full transition-all duration-700 ease-out shadow-lg relative"
        :style="{ width: `${progress}%` }"
      >
        <div class="absolute inset-0 bg-gradient-to-r from-emerald-300 to-blue-300 rounded-full opacity-50 animate-pulse"></div>
      </div>
    </div>
    
    <!-- Indicador de paso actual -->
    <div class="text-center mt-3">
      <span class="text-sm text-gray-400 font-medium">
        Paso {{ currentStep }} de {{ totalSteps }} - {{ stepTitles[currentStep - 1] }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  currentStep: {
    type: Number,
    required: true
  },
  totalSteps: {
    type: Number,
    default: 4
  }
});

defineEmits(['goToStep']);

const stepTitles = [
  'Informaci+¦n B+ísica',
  'Caracter+¡sticas',
  'Evaluaci+¦n IA',
  'Confirmaci+¦n'
];

const progress = computed(() => {
  return (props.currentStep / props.totalSteps) * 100;
});
</script>

<style scoped>
@keyframes pulse-ring {
  0% {
    transform: scale(0.33);
    opacity: 1;
  }
  80%, 100% {
    transform: scale(1.33);
    opacity: 0;
  }
}

.animate-pulse-ring {
  animation: pulse-ring 1.5s ease-out infinite;
}
</style>
