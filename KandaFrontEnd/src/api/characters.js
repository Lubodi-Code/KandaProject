import apiClient from './apiClient';

export const characterService = {
  list() {
    return apiClient.get('/api/characters/');
  },
  create(data) {
    return apiClient.post('/api/characters/', data);
  },
  update(id, data) {
    return apiClient.put(`/api/characters/${id}/`, data);
  },
  delete(id) {
    return apiClient.delete(`/api/characters/${id}/`);
  },
  createDefault() {
    return apiClient.post('/api/characters/create-default/');
  }
};
