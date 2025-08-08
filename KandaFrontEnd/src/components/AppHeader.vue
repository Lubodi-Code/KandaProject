<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import tokenManager from '../utils/tokenManager'
import { authService } from '../api/auth'

const router = useRouter()

const isAuthed = computed(() => tokenManager.isAuthenticated())

const logout = () => {
  authService.logout()
  router.push('/login')
}
</script>

<template>
  <header class="w-full bg-gray-900 text-white border-b border-gray-800">
    <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
      <div class="flex items-center space-x-2 select-none">
        <span class="text-lg font-bold">Kanda</span>
        <span class="text-sm text-gray-400">Storytelling</span>
      </div>
      <div v-if="isAuthed" class="flex items-center space-x-3">
        <button
          @click="logout"
          class="bg-red-500 hover:bg-red-600 text-white px-3 py-1.5 rounded-md text-sm transition-colors"
        >
          Cerrar sesi+¦n
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped>
</style>
