import { ref } from 'vue'
import { characterService } from '../api/characters'

export function useCharacterAI() {
  // Estados reactivos
  const hasRequestedEvaluation = ref(false)
  const isLoadingEvaluation = ref(false)
  const aiEvaluation = ref(null)
  const evaluationError = ref(null)

  // Funci+¦n para preparar datos para evaluaci+¦n
  const prepareDataForEvaluation = (characterData) => {
    return {
      name: characterData.name || '',
      age: parseInt(characterData.age) || 0,
      archetype: characterData.archetype || 'Aventurero',
      gender: characterData.gender || '',
      physical_description: characterData.physical_description || '',
      personality: characterData.personality || '',
      weaknesses: characterData.weaknesses || '',
      history: characterData.history || '',
      special_abilities: characterData.special_abilities || '',
      goals: characterData.goals || ''
    }
  }

  // Funci+¦n para solicitar evaluaci+¦n de IA
  const requestAiEvaluation = async (characterData) => {
    if (!characterData || isLoadingEvaluation.value) return

    isLoadingEvaluation.value = true
    evaluationError.value = null

    try {
      // Preparar solo los datos necesarios para la evaluaci+¦n
      const evaluationData = prepareDataForEvaluation(characterData)
      console.log('Enviando datos para evaluaci+¦n:', evaluationData)
      
      const response = await characterService.evaluateCharacter(evaluationData)
      aiEvaluation.value = response.data
      hasRequestedEvaluation.value = true
      return response.data
    } catch (error) {
      console.error('Error evaluating character:', error)
      evaluationError.value = error.response?.data?.error || error.response?.data?.message || 'Error al evaluar el personaje'
      throw error
    } finally {
      isLoadingEvaluation.value = false
    }
  }

  // Funci+¦n para aceptar sugerencias de IA
  const acceptAiSuggestions = (formData) => {
    if (!aiEvaluation.value || !formData) {
      console.warn('No hay evaluaci+¦n o datos del formulario para aplicar')
      return
    }

    const evaluation = aiEvaluation.value
    console.log('Aplicando sugerencias de IA:', evaluation)

    // Aplicar sugerencias si existen
    if (evaluation.suggested_personality) {
      formData.personality = evaluation.suggested_personality
      console.log('Personalidad actualizada:', evaluation.suggested_personality)
    }
    if (evaluation.suggested_strengths) {
      formData.strengths = evaluation.suggested_strengths
      console.log('Fortalezas actualizadas:', evaluation.suggested_strengths)
    }
    if (evaluation.suggested_weaknesses) {
      formData.weaknesses = evaluation.suggested_weaknesses
      console.log('Debilidades actualizadas:', evaluation.suggested_weaknesses)
    }
    if (evaluation.suggested_history) {
      formData.history = evaluation.suggested_history
      console.log('Historia actualizada:', evaluation.suggested_history)
    }

    // Tambi+®n aplicar otras sugerencias si est+ín disponibles
    if (evaluation.suggestions) {
      const suggestions = evaluation.suggestions
      if (suggestions.personality) formData.personality = suggestions.personality
      if (suggestions.strengths) formData.strengths = suggestions.strengths
      if (suggestions.weaknesses) formData.weaknesses = suggestions.weaknesses
      if (suggestions.history) formData.history = suggestions.history
    }
  }

  // Funci+¦n para rechazar sugerencias de IA
  const rejectAiSuggestions = () => {
    // No hacer nada, mantener los valores actuales del formulario
    console.log('Sugerencias de IA rechazadas')
  }

  // Funci+¦n para generar trasfondo del personaje
  const generateCharacterBackground = async (characterData) => {
    if (!characterData || !characterData.name) {
      throw new Error('Datos del personaje incompletos')
    }

    try {
      const response = await characterService.generateBackground({
        name: characterData.name,
        personality: characterData.personality || '',
        strengths: characterData.strengths || '',
        weaknesses: characterData.weaknesses || ''
      })
      
      return response.data?.background || response.data
    } catch (error) {
      console.error('Error generating background:', error)
      
      // Fallback con trasfondo generado localmente
      const fallbackBackground = generateFallbackBackground(characterData)
      return fallbackBackground
    }
  }

  // Funci+¦n de respaldo para generar trasfondo
  const generateFallbackBackground = (characterData) => {
    const { name, personality, strengths, weaknesses } = characterData
    
    const backgrounds = [
      `${name} creci+¦ en un peque+¦o pueblo donde aprendi+¦ el valor del trabajo duro. Su personalidad ${personality} se forj+¦ a trav+®s de experiencias que moldearon su car+ícter. Sus fortalezas en ${strengths} la ayudaron a superar las dificultades, aunque sus debilidades en ${weaknesses} a veces le trajeron complicaciones.`,
      
      `Desde joven, ${name} mostr+¦ una personalidad ${personality} que la distingu+¡a del resto. A lo largo de los a+¦os, desarroll+¦ habilidades excepcionales en ${strengths}, convirti+®ndose en alguien respetado por sus capacidades. Sin embargo, sus retos con ${weaknesses} le ense+¦aron importantes lecciones de humildad.`,
      
      `${name} es conocido por su naturaleza ${personality}, una caracter+¡stica que se desarroll+¦ durante sus a+¦os formativos. Su dominio en ${strengths} le ha abierto muchas puertas, pero ha tenido que trabajar constantemente para superar sus limitaciones con ${weaknesses}.`
    ]
    
    return backgrounds[Math.floor(Math.random() * backgrounds.length)]
  }

  // Funci+¦n para resetear el estado de evaluaci+¦n
  const resetEvaluationState = () => {
    hasRequestedEvaluation.value = false
    aiEvaluation.value = null
    evaluationError.value = null
    console.log('Estado de evaluaci+¦n reseteado')
  }

  return {
    // Estados
    hasRequestedEvaluation,
    isLoadingEvaluation,
    aiEvaluation,
    evaluationError,
    
    // M+®todos
    requestAiEvaluation,
    acceptAiSuggestions,
    rejectAiSuggestions,
    generateCharacterBackground,
    resetEvaluationState
  }
}
