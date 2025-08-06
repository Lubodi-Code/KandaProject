<template>
  <div class="characters-view">
    <h1>Gestión de Personajes</h1>
    <p>Aquí puedes ver y gestionar tus personajes.</p>
    <CharacterFormModal @character-saved="handleCharacterSaved" />
  </div>
</template>

<script>
import CharacterFormModal from '@/components/CharacterFormModal.vue';

export default {
  name: 'CharactersView',
  components: {
    CharacterFormModal
  },
  methods: {
    handleCharacterSaved(characterData) {
      console.log('Personaje guardado:', characterData);
      // Aquí podrías añadir lógica para enviar los datos al backend,
      // actualizar una lista de personajes, cerrar el modal, etc.
      alert('Personaje guardado. Revisa la consola para ver los datos.');
    }
  }
};
</script>

<style scoped>
.characters-view {
  padding: 20px;
}
</style>
