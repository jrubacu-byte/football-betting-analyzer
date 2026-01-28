import requests
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LLMAnalysisClient:
    def __init__(self, api_key: str, base_url: str = "https://routellm.abacus.ai/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def analyze_match(self, match_name: str, user_odds: Dict[str, float]) -> Dict[str, Any]:
        """
        Llama a la LLM para analizar un partido.
        Input: match_name (ej: "Ajax vs Olympiacos"), user_odds (cuotas del bookmaker)
        Output: JSON con análisis completo
        """
        prompt = self._build_analysis_prompt(match_name, user_odds)
        
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }

        try:
            logger.info(f"Llamando a LLM API: {self.base_url}/chat/completions")
            logger.info(f"API Key presente: {bool(self.api_key)}, Longitud: {len(self.api_key) if self.api_key else 0}")
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            logger.info(f"Respuesta HTTP Status: {response.status_code}")
            
            # Log response body for debugging if error
            if response.status_code != 200:
                logger.error(f"Respuesta error: {response.text}")
            
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Respuesta JSON recibida con {len(result.get('choices', []))} choices")
            
            analysis_text = result["choices"][0]["message"]["content"]
            logger.info(f"Texto de análisis recibido (primeros 200 chars): {analysis_text[:200]}")
            
            # Parsear JSON de la respuesta
            parsed = self._parse_analysis(analysis_text)
            logger.info(f"JSON parseado exitosamente: {list(parsed.keys()) if isinstance(parsed, dict) else 'No dict'}")
            return parsed
        
        except requests.exceptions.RequestException as e:
            logger.exception(f"Error en llamada a LLM API: {str(e)}")
            return {"error": f"LLM API Error: {str(e)}"}
        except (KeyError, IndexError) as e:
            logger.exception(f"Error parseando respuesta de LLM: {str(e)}")
            return {"error": f"Error parseando respuesta: {str(e)}"}
        except Exception as e:
            logger.exception(f"Error inesperado en analyze_match: {str(e)}")
            return {"error": f"Error inesperado: {str(e)}"}

    def _build_analysis_prompt(self, match_name: str, user_odds: Dict[str, float]) -> str:
        odds_str = "\n".join([f"  {k}: {v}" for k, v in user_odds.items()])
        return f"""
Analiza este partido de fútbol:
PARTIDO: {match_name}

CUOTAS DEL BOOKMAKER:
{odds_str}

TAREA:
1. Busca datos actualizados: forma reciente (últimos 5 partidos), lesiones, alineaciones, árbitro, xG.
2. Calcula los parámetros λ (goles esperados) para ambos equipos.
3. Devuelve un JSON con:
   - Probabilidades reales para 1X2, Goles, Córners, Tarjetas
   - Cuotas justas (1/probabilidad)
   - Comparación con cuotas del bookmaker
   - Apuesta recomendada (si hay EV+)
   - Insights clave (lesiones, árbitro, forma)

FORMATO JSON OBLIGATORIO:
{{
  "match": "{match_name}",
  "exp_goals_home": 0.0,
  "exp_goals_away": 0.0,
  "exp_corners": 0.0,
  "exp_cards": 0.0,
  "key_insights": ["insight1", "insight2", "insight3"],
  "referee_info": "nombre y media de tarjetas"
}}
"""

    def _get_system_prompt(self) -> str:
        from backend.utils.prompts import SYSTEM_PROMPT
        return SYSTEM_PROMPT

    def _parse_analysis(self, text: str) -> Dict[str, Any]:
        """Extrae el JSON de la respuesta de la LLM."""
        try:
            # Busca el JSON en la respuesta
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                json_str = text[start:end]
                logger.info(f"JSON extraído para parsear (primeros 300 chars): {json_str[:300]}")
                parsed = json.loads(json_str)
                return parsed
            else:
                logger.error(f"No se encontró JSON en la respuesta. Texto completo: {text}")
                return {"error": "No se encontró JSON en la respuesta de la LLM"}
        except json.JSONDecodeError as e:
            logger.exception(f"Error decodificando JSON: {str(e)}")
            logger.error(f"Texto que causó el error: {text}")
            return {"error": f"No se pudo parsear la respuesta de la LLM: {str(e)}"}
