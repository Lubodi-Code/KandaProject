<template>
  <div class="space-y-6">
    <div class="text-center mb-8">
      <h3 class="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-blue-400 bg-clip-text text-transparent">
        Informaci+好 B+疄ica
      </h3>
      <p class="text-gray-400 mt-2">Comencemos con los datos fundamentales de tu personaje</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Nombre -->
      <div class="space-y-2">
        <label class="text-sm font-medium text-gray-300 flex items-center">
          <svg class="w-4 h-4 mr-2 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          Nombre *
        </label>
        <input
          v-model="form.name"
          type="text"
          required
          placeholder="Ej: Aragorn, Hermione, Luke..."
          :class="inputClasses"
          @blur="validateField('name')"
        >
        <p v-if="errors.name" class="text-red-400 text-xs mt-1">{{ errors.name }}</p>
      </div>

      <!-- Edad -->
      <div class="space-y-2">
        <label class="text-sm font-medium text-gray-300 flex items-center">
          <svg class="w-4 h-4 mr-2 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          Edad *
        </label>
        <input
          v-model.number="form.age"
          type="number"
          required
          min="1"
          max="9999"
          placeholder="Ej: 25"
          :class="inputClasses"
          @blur="validateField('age')"
        >
        <p v-if="errors.age" class="text-red-400 text-xs mt-1">{{ errors.age }}</p>
      </div>

      <!-- G+峪ero -->
      <div class="space-y-2">
        <label class="text-sm font-medium text-gray-300 flex items-center">
          <svg class="w-4 h-4 mr-2 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
          </svg>
          G+峪ero *
        </label>
        <select
          v-model="form.gender"
          required
          :class="inputClasses"
          @change="validateField('gender')"
        >
          <option value="">Selecciona un g+峪ero</option>
          <option value="Masculino">Masculino</option>
          <option value="Femenino">Femenino</option>
          <option value="No binario">No binario</option>
          <option value="Otro">Otro</option>
        </select>
        <p v-if="errors.gender" class="text-red-400 text-xs mt-1">{{ errors.gender }}</p>
      </div>
    </div>

    <!-- Descripci+好 F+︿ica -->
    <div class="space-y-2">
      <label class="text-sm font-medium text-gray-300 flex items-center">
        <svg class="w-4 h-4 mr-2 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        </svg>
        Descripci+好 F+︿ica *
      </label>
      <textarea
        v-model="form.physical_description"
        required
        rows="4"
        placeholder="Describe la apariencia f+︿ica de tu personaje: altura, complexi+好, color de cabello, ojos, caracter+︿ticas distintivas..."
        :class="[inputClasses, 'resize-none']"
        @blur="validateField('physical_description')"
      ></textarea>
      <p v-if="errors.physical_description" class="text-red-400 text-xs mt-1">{{ errors.physical_description }}</p>
      <div class="flex justify-between text-xs text-gray-500">
        <span>M+》imo 10 caracteres</span>
        <span>{{ form.physical_description?.length || 0 }}/500</span>
      </div>
    </div>

    <!-- Stats Preview -->
    <div v-if="isFormValid" class="mt-8 p-6 bg-gradient-to-r from-emerald-900/20 to-blue-900/20 rounded-xl border border-emerald-500/20">
      <h4 class="text-lg font-semibold text-emerald-400 mb-4 flex items-center">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        Vista Previa
      </h4>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
        <div>
          <span class="text-gray-400">Nombre:</span>
          <p class="text-white font-medium">{{ form.name }}</p>
        </div>
        <div>
          <span class="text-gray-400">Edad:</span>
          <p class="text-white font-medium">{{ form.age }} a+她s</p>
        </div>
        <div>
          <span class="text-gray-400">G+峪ero:</span>
          <p class="text-white font-medium">{{ form.gender }}</p>
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
  }
});

const emit = defineEmits(['update:modelValue', 'validation-change']);

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
    case 'name':
      if (!form.value.name || form.value.name.trim().length < 2) {
        errors[field] = 'El nombre debe tener al menos 2 caracteres';
      } else {
        delete errors[field];
      }
      break;
    case 'age':
      if (!form.value.age || form.value.age < 1 || form.value.age > 9999) {
        errors[field] = 'La edad debe estar entre 1 y 9999 a+她s';
      } else {
        delete errors[field];
      }
      break;
    case 'gender':
      if (!form.value.gender) {
        errors[field] = 'El g+峪ero es requerido';
      } else {
        delete errors[field];
      }
      break;
    case 'physical_description':
      if (!form.value.physical_description || form.value.physical_description.trim().length < 10) {
        errors[field] = 'La descripci+好 f+︿ica debe tener al menos 10 caracteres';
      } else if (form.value.physical_description.length > 500) {
        errors[field] = 'La descripci+好 f+︿ica no debe exceder 500 caracteres';
      } else {
        delete errors[field];
      }
      break;
  }
  
  emit('validation-change', isFormValid.value);
};

const isFormValid = computed(() => {
  return form.value.name?.trim().length >= 2 &&
         form.value.age >= 1 && form.value.age <= 9999 &&
         form.value.gender &&
         form.value.physical_description?.trim().length >= 10 &&
         Object.keys(errors).length === 0;
});

// Watchers para validaci+好 en tiempo real
import { watch } from 'vue';

watch(() => form.value.name, () => validateField('name'));
watch(() => form.value.age, () => validateField('age'));
watch(() => form.value.gender, () => validateField('gender'));
watch(() => form.value.physical_description, () => validateField('physical_description'));
</script>
