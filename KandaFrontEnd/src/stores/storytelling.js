import { defineStore } from 'pinia';
import { universeAPI, roomAPI, participantAPI } from '../api/storytelling.js';

export const useUniverseStore = defineStore('universe', {
  state: () => ({
    universes: [],
    currentUniverse: null,
    loading: false,
    error: null
  }),

  getters: {
    publicUniverses: (state) => state.universes.filter(u => u.is_public),
    userUniverses: (state) => state.universes.filter(u => !u.is_public)
  },

  actions: {
    async fetchUniverses() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await universeAPI.getAll();
        this.universes = response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al cargar universos';
        console.error('Error fetching universes:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchUniverse(id) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await universeAPI.getById(id);
        this.currentUniverse = response.data;
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al cargar universo';
        console.error('Error fetching universe:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async createUniverse(universeData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await universeAPI.create(universeData);
        this.universes.unshift(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al crear universo';
        console.error('Error creating universe:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateUniverse(id, universeData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await universeAPI.update(id, universeData);
        const index = this.universes.findIndex(u => u.id === id);
        if (index !== -1) {
          this.universes[index] = response.data;
        }
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al actualizar universo';
        console.error('Error updating universe:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteUniverse(id) {
      this.loading = true;
      this.error = null;
      
      try {
        await universeAPI.delete(id);
        this.universes = this.universes.filter(u => u.id !== id);
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al eliminar universo';
        console.error('Error deleting universe:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    clearError() {
      this.error = null;
    }
  }
});

export const useRoomStore = defineStore('room', {
  state: () => ({
    publicRooms: [],
    myRooms: [],
    joinedRooms: [],
    currentRoom: null,
    participants: [],
    loading: false,
    error: null
  }),

  getters: {
    availableRooms: (state) => state.publicRooms.filter(r => r.status === 'waiting'),
    currentRoomPlayerCount: (state) => state.currentRoom?.player_count || 0,
    isCurrentRoomAdmin: (state) => {
      if (!state.currentRoom) return false;
      const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
      return state.currentRoom.admin === currentUser.id;
    }
  },

  actions: {
    async fetchPublicRooms() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await roomAPI.getPublicRooms();
        this.publicRooms = response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al cargar salas';
        console.error('Error fetching public rooms:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchMyRooms() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await roomAPI.getMyRooms();
        this.myRooms = response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al cargar mis salas';
        console.error('Error fetching my rooms:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchJoinedRooms() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await roomAPI.getJoinedRooms();
        this.joinedRooms = response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al cargar salas unidas';
        console.error('Error fetching joined rooms:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchRoom(id) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await roomAPI.getById(id);
        this.currentRoom = response.data;
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al cargar sala';
        console.error('Error fetching room:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async createRoom(roomData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await roomAPI.create(roomData);
        this.myRooms.unshift(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al crear sala';
        console.error('Error creating room:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async joinRoom(id, accessCode = null) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await roomAPI.join(id, accessCode);
        this.currentRoom = response.data;
        
        // A+¦adir a joinedRooms si no est+í ya
        if (!this.joinedRooms.find(r => r.id === id)) {
          this.joinedRooms.unshift(response.data);
        }
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al unirse a la sala';
        console.error('Error joining room:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async joinRoomWithCode(accessCode) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await roomAPI.joinWithCode(accessCode);
        this.currentRoom = response.data;
        
        // A+¦adir a joinedRooms
        if (!this.joinedRooms.find(r => r.id === response.data.id)) {
          this.joinedRooms.unshift(response.data);
        }
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al unirse con c+¦digo';
        console.error('Error joining room with code:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async leaveRoom(id) {
      this.loading = true;
      this.error = null;
      
      try {
        await roomAPI.leave(id);
        
        // Remover de joinedRooms
        this.joinedRooms = this.joinedRooms.filter(r => r.id !== id);
        
        // Si es la sala actual, limpiarla
        if (this.currentRoom?.id === id) {
          this.currentRoom = null;
          this.participants = [];
        }
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al salir de la sala';
        console.error('Error leaving room:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async startGame(id) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await roomAPI.startGame(id);
        
        // Actualizar estado de la sala
        if (this.currentRoom?.id === id) {
          this.currentRoom.status = 'playing';
        }
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al iniciar el juego';
        console.error('Error starting game:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchParticipants(roomId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await participantAPI.getByRoom(roomId);
        this.participants = response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al cargar participantes';
        console.error('Error fetching participants:', error);
      } finally {
        this.loading = false;
      }
    },

    async addCharactersToRoom(roomId, characterIds) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await participantAPI.addToRoom(roomId, characterIds);
        this.participants.push(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al a+¦adir personajes';
        console.error('Error adding characters to room:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async setParticipantReady(participantId, isReady = true) {
      this.loading = true;
      this.error = null;
      try {
        const response = await participantAPI.setReady(participantId, isReady);
        // Update local participant state
        const idx = this.participants.findIndex(p => p.id === participantId);
        if (idx !== -1) this.participants[idx] = response.data;
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Error al marcar listo';
        console.error('Error setting participant ready:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    clearError() {
      this.error = null;
    },

    clearCurrentRoom() {
      this.currentRoom = null;
      this.participants = [];
    }
  }
});
