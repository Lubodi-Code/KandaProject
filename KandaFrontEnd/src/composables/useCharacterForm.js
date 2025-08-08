import { ref } from 'vue';
import { characterService } from '../api/characters';

export function useCharacterForm(character) {
  const formData = ref({
    name: '',
    age: '',
    gender: '',
    physical_description: '',
    personality: '',
    history: '',
    strengths: '',
    weaknesses: '',
    special_abilities: '',
    goals: '',
    archetype: 'Aventurero' // Valor por defecto para el backend
  });

  // Funci+好 para resetear el formulario
  const resetForm = () => {
    formData.value = {
      name: '',
      age: '',
      gender: '',
      physical_description: '',
      personality: '',
      history: '',
      strengths: '',
      weaknesses: '',
      special_abilities: '',
      goals: '',
      archetype: 'Aventurero'
    };
  };

  // Funci+好 para inicializar el formulario
  const initializeForm = async () => {
    if (character) {
      formData.value = {
        name: character.name || '',
        age: character.age || '',
        gender: character.gender || '',
        physical_description: character.physical_description || '',
        personality: character.personality || '',
        history: character.history || '',
        strengths: character.strengths || '',
        weaknesses: character.weaknesses || '',
        special_abilities: character.special_abilities || '',
        goals: character.goals || '',
        archetype: character.archetype || 'Aventurero'
      };
    } else {
      resetForm();
    }
  };

  // Funci+好 para crear el payload
  const createCharacterPayload = (data, aiEvaluation) => {
    console.log('Creating character payload from:', data);
    
    // Helper function to convert string to array
    const stringToArray = (str) => {
      if (!str) return [];
      return str.split(',').map(item => item.trim()).filter(item => item.length > 0);
    };
    
    const payload = {
      name: data.name,
      age: data.age,
      gender: data.gender,
      archetype: data.archetype,
      // Convert string fields to expected format
      physical_traits: data.physical_description ? [data.physical_description] : [],
      personality_traits: data.personality ? [data.personality] : [],
      weaknesses: stringToArray(data.weaknesses),
      background: data.history || "",
      special_abilities: data.special_abilities || "",
      goals: data.goals || "",
      aiFilter: aiEvaluation ? {
        overall_score: aiEvaluation.overall_score,
        comments: aiEvaluation.comments,
        suggested_improvements: aiEvaluation.suggested_improvements,
        powerLevel: aiEvaluation.overall_score || 5,
        strengths: stringToArray(data.strengths),
        flaws: stringToArray(data.weaknesses),
        accepted: true
      } : {
        powerLevel: 5,
        strengths: stringToArray(data.strengths),
        flaws: stringToArray(data.weaknesses),
        accepted: false
      }
    };
    
    console.log('Created payload:', payload);
    return payload;
  };

  // Funci+好 para guardar el personaje
  const saveCharacter = async (payload, isEditing) => {
    console.log('saveCharacter called with:', { payload, isEditing });
    try {
      if (isEditing && character?.id) {
        console.log('Updating character with ID:', character.id);
        const result = await characterService.updateCharacter(character.id, payload);
        console.log('Update result:', result);
        return result;
      } else {
        console.log('Creating new character using TEST endpoint');
        // TEMPORAL: Usar endpoint de testing sin autenticaci+好
        const result = await characterService.createCharacterTest(payload);
        console.log('Create result:', result);
        return result;
      }
    } catch (error) {
      console.error('Error saving character:', error);
      console.error('Error details:', {
        message: error.message,
        response: error.response,
        status: error.response?.status,
        data: error.response?.data
      });
      throw error;
    }
  };

  return {
    formData,
    initializeForm,
    createCharacterPayload,
    saveCharacter,
    resetForm
  };
}
