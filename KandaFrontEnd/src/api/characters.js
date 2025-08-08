import apiClient from './apiClient';

export const characterService = {
  // Verificar conectividad con el backend
  testConnection() {
  return apiClient.get('/system/health/');
  },
  
  // Verificar autenticaci+¦n
  testAuth() {
    return apiClient.get('/test-auth/');
  },
  
  // Obtener lista de personajes
  list() {
  return apiClient.get('/characters/');
  },
  
  // Crear personaje
  create(data) {
  return apiClient.post('/characters/', data);
  },
  
  // Actualizar personaje
  update(id, data) {
  return apiClient.put(`/characters/${id}/`, data);
  },
  
  // Eliminar personaje
  delete(id) {
  return apiClient.delete(`/characters/${id}/`);
  },
  
  // Crear personaje por defecto
  createDefault() {
  return apiClient.post('/characters/create-default/');
  },
  
  // Evaluar personaje con IA sin guardar
  evaluateWithAI(data) {
  return apiClient.post('/characters/evaluate/', data);
  },

  // Evaluar personaje con IA (alias para evaluateWithAI)
  evaluateCharacter(data) {
    return this.evaluateWithAI(data);
  },

  // Generar trasfondo autom+ítico
  generateBackground(data) {
  return apiClient.post('/characters/generate-background/', data);
  },

  // Crear personaje (alias para create)
  createCharacter(data) {
    return this.create(data);
  },

  // Actualizar personaje (alias para update)
  updateCharacter(id, data) {
    return this.update(id, data);
  },

  // TEMPORAL: Crear personaje sin autenticaci+¦n para testing
  createCharacterTest(data) {
  return apiClient.post('/characters/test-create/', data);
  }
};
