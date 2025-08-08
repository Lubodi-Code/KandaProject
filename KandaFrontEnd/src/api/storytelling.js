import apiClient from './apiClient.js';

export const universeAPI = {
  // Obtener todos los universos
  getAll() {
    return apiClient.get('/universes/');
  },

  // Obtener un universo espec+〕ico
  getById(id) {
    return apiClient.get(`/universes/${id}/`);
  },

  // Crear nuevo universo (admin only)
  create(universeData) {
    return apiClient.post('/universes/', universeData);
  },

  // Actualizar universo
  update(id, universeData) {
    return apiClient.put(`/universes/${id}/`, universeData);
  },

  // Eliminar universo
  delete(id) {
    return apiClient.delete(`/universes/${id}/`);
  }
};

export const roomAPI = {
  // Obtener salas p+在licas
  getPublicRooms() {
    return apiClient.get('/rooms/');
  },

  // Obtener mis salas (como admin)
  getMyRooms() {
    return apiClient.get('/rooms/my_rooms/');
  },

  // Obtener salas donde soy participante
  getJoinedRooms() {
    return apiClient.get('/rooms/joined_rooms/');
  },

  // Obtener una sala espec+〕ica
  getById(id) {
    return apiClient.get(`/rooms/${id}/`);
  },

  // Crear nueva sala
  create(roomData) {
    return apiClient.post('/rooms/', roomData);
  },

  // Actualizar sala
  update(id, roomData) {
    return apiClient.put(`/rooms/${id}/`, roomData);
  },

  // Unirse a sala p+在lica
  join(id, accessCode = null) {
    const data = accessCode ? { access_code: accessCode } : {};
    return apiClient.post(`/rooms/${id}/join/`, data);
  },

  // Unirse con c+圬igo de acceso
  joinWithCode(accessCode) {
    return apiClient.post('/rooms/join-with-code/', { access_code: accessCode });
  },

  // Salir de sala
  leave(id) {
    return apiClient.post(`/rooms/${id}/leave/`);
  },

  // Iniciar juego (admin only)
  startGame(id) {
    return apiClient.post(`/rooms/${id}/start_game/`);
  }
};

export const participantAPI = {
  // A+地dir personajes a una sala
  addToRoom(roomId, characterIds) {
    return apiClient.post('/room-participants/', {
      room: roomId,
      characters: characterIds
    });
  },

  // Obtener participantes de una sala
  getByRoom(roomId) {
    return apiClient.get(`/room-participants/by_room/?room_id=${roomId}`);
  },

  // Marcar como listo
  setReady(participantId, isReady = true) {
    return apiClient.patch(`/room-participants/${participantId}/`, {
      is_ready: isReady
    });
  }
};

export const storyAPI = {
  // Obtener historia de una sala
  getByRoom(roomId) {
    return apiClient.get(`/stories/?room=${roomId}`);
  },

  // Obtener historia espec+〕ica
  getById(id) {
    return apiClient.get(`/stories/${id}/`);
  }
};

export const chapterAPI = {
  // Obtener cap+﹀ulos de una historia
  getByStory(storyId) {
    return apiClient.get(`/chapters/?story=${storyId}`);
  },

  // Obtener cap+﹀ulo espec+〕ico
  getById(id) {
    return apiClient.get(`/chapters/${id}/`);
  }
};

export const actionAPI = {
  // Enviar acci+好 de jugador
  submit(chapterId, characterId, actionText) {
    return apiClient.post('/player-actions/', {
      chapter: chapterId,
      character: characterId,
      action_text: actionText
    });
  },

  // Obtener acciones de un cap+﹀ulo
  getByChapter(chapterId) {
    return apiClient.get(`/player-actions/?chapter=${chapterId}`);
  }
};

// Servicio combinado de storytelling para las vistas
export const storytellingService = {
  // Universos
  getUniverses: () => universeAPI.getAll(),
  createUniverse: (data) => universeAPI.create(data),
  updateUniverse: (id, data) => universeAPI.update(id, data),
  deleteUniverse: (id) => universeAPI.delete(id),

  // Salas
  getPublicRooms: () => roomAPI.getPublicRooms(),
  getMyRooms: () => roomAPI.getMyRooms(),
  getJoinedRooms: () => roomAPI.getJoinedRooms(),
  getRoom: (id) => roomAPI.getById(id),
  createRoom: (data) => roomAPI.create(data),
  joinRoom: (accessCode) => roomAPI.joinWithCode(accessCode),
  leaveRoom: (id) => roomAPI.leave(id),
  startGame: (id) => roomAPI.startGame(id),
  addCharactersToRoom: (roomId, characterIds) => participantAPI.addToRoom(roomId, characterIds),

  // Participantes
  getRoomParticipants: (roomId) => participantAPI.getByRoom(roomId),

  // Historia y cap+﹀ulos
  getCurrentStory: (roomId) => storyAPI.getByRoom(roomId),
  getStory: (id) => storyAPI.getById(id),
  getStoryChapters: (storyId) => chapterAPI.getByStory(storyId),
  getChapter: (id) => chapterAPI.getById(id),

  // Acciones
  submitPlayerAction: (roomId, actionData) => {
    return apiClient.post(`/rooms/${roomId}/submit_action/`, actionData);
  },

  // IA Narrativa
  generateNarrative: (roomId) => {
    return apiClient.post(`/rooms/${roomId}/generate_narrative/`);
  }
};
