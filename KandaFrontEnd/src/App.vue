<script setup>
import { RouterView, useRoute } from 'vue-router'
import AppHeader from './components/AppHeader.vue'

const route = useRoute()
const hideHeaderRoutes = new Set(['login', 'register', 'activate', 'activate-email', 'activate-invalid', 'resend-activation'])
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader v-if="!hideHeaderRoutes.has(route.name)" />
    <main class="flex-1">
      <RouterView />
    </main>
  </div>
 </template>
