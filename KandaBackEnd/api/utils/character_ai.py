import json
import logging
import openai
from django.conf import settings

logger = logging.getLogger(__name__)


def generate_ai_filter(character):
    """Generate strengths and flaws for a character using OpenAI."""
    api_key = getattr(settings, "OPENAI_API_KEY", None)
    if not api_key:
        logger.warning("OpenAI API key not configured.")
        return None

    openai.api_key = api_key
    model = getattr(settings, "OPENAI_MODEL", "gpt-3.5-turbo")
    physical = ", ".join(character.physical_traits or []) or "ninguno"
    personality = ", ".join(character.personality_traits or []) or "ninguno"
    background = character.background or "N/A"
    prompt = (
        "Equilibra el siguiente personaje de rol. Añade debilidades que compensen sus fortalezas y limita sus ventajas. "
        f"Aspectos físicos: {physical}. "
        f"Aspectos de personalidad: {personality}. "
        f"Historia o antecedentes: {background}. "
        "Devuelve únicamente un JSON con dos listas, 'strengths' y 'flaws', cada una con hasta 3 elementos."
    )

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Eres un experto en equilibrar personajes de juegos de rol."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        return {
            "strengths": data.get("strengths", []),
            "flaws": data.get("flaws", []),
        }
    except Exception as exc:
        logger.error("Error generating AI filter: %s", exc)
        return None
