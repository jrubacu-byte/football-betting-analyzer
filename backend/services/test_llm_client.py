import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.services.llm_client import LLMAnalysisClient


class TestLLMAnalysisClient:
    """Tests para el cliente LLM."""
    
    def test_client_initialization(self):
        """Verifica que el cliente se inicializa correctamente."""
        client = LLMAnalysisClient(api_key="test-key")
        
        assert client.api_key == "test-key"
        assert client.base_url == "https://routellm.abacus.ai/v1"
        assert "Authorization" in client.headers
        assert client.headers["Authorization"] == "Bearer test-key"
        assert client.headers["Content-Type"] == "application/json"
    
    def test_client_custom_base_url(self):
        """Verifica que se puede usar una URL base personalizada."""
        client = LLMAnalysisClient(api_key="test-key", base_url="https://custom.api.com/v1")
        
        assert client.base_url == "https://custom.api.com/v1"
    
    def test_build_analysis_prompt(self):
        """Verifica que el prompt se construye correctamente."""
        client = LLMAnalysisClient(api_key="test-key")
        
        user_odds = {
            "1X2_Home": 1.85,
            "1X2_Draw": 3.50,
            "1X2_Away": 4.20
        }
        
        prompt = client._build_analysis_prompt("Ajax vs Olympiacos", user_odds)
        
        assert "Ajax vs Olympiacos" in prompt
        assert "1X2_Home: 1.85" in prompt
        assert "1X2_Draw: 3.5" in prompt
        assert "1X2_Away: 4.2" in prompt
        assert "CUOTAS DEL BOOKMAKER" in prompt
        assert "FORMATO JSON OBLIGATORIO" in prompt
    
    def test_parse_analysis_valid_json(self):
        """Verifica que el parsing de JSON válido funciona."""
        client = LLMAnalysisClient(api_key="test-key")
        
        response_text = '''
        Aquí está mi análisis:
        {
          "match": "Ajax vs Olympiacos",
          "exp_goals_home": 1.8,
          "exp_goals_away": 0.9,
          "exp_corners": 10.5,
          "exp_cards": 3.8,
          "key_insights": ["Ajax en buena forma", "Olympiacos con lesiones"],
          "referee_info": "Carlos del Cerro - 4.5 tarjetas/partido"
        }
        '''
        
        result = client._parse_analysis(response_text)
        
        assert result["match"] == "Ajax vs Olympiacos"
        assert result["exp_goals_home"] == 1.8
        assert result["exp_goals_away"] == 0.9
        assert result["exp_corners"] == 10.5
        assert result["exp_cards"] == 3.8
        assert len(result["key_insights"]) == 2
    
    def test_parse_analysis_only_json(self):
        """Verifica que parsea JSON sin texto adicional."""
        client = LLMAnalysisClient(api_key="test-key")
        
        response_text = '{"match": "Test Match", "exp_goals_home": 1.5, "exp_goals_away": 1.0}'
        
        result = client._parse_analysis(response_text)
        
        assert result["match"] == "Test Match"
        assert result["exp_goals_home"] == 1.5
    
    def test_parse_analysis_invalid_json(self):
        """Verifica que el parsing de JSON inválido devuelve error."""
        client = LLMAnalysisClient(api_key="test-key")
        
        response_text = "Este es un texto sin JSON válido"
        
        result = client._parse_analysis(response_text)
        
        assert "error" in result
        assert "No se pudo parsear" in result["error"]
    
    def test_parse_analysis_malformed_json(self):
        """Verifica que JSON malformado devuelve error."""
        client = LLMAnalysisClient(api_key="test-key")
        
        response_text = '{"match": "Test", "invalid":'
        
        result = client._parse_analysis(response_text)
        
        assert "error" in result
    
    @patch('backend.services.llm_client.requests.post')
    def test_analyze_match_success(self, mock_post):
        """Verifica que analyze_match funciona con respuesta exitosa."""
        # Mock de respuesta exitosa
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"match": "Ajax vs Olympiacos", "exp_goals_home": 1.8, "exp_goals_away": 0.9}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        client = LLMAnalysisClient(api_key="test-key")
        
        with patch.object(client, '_get_system_prompt', return_value="Test system prompt"):
            result = client.analyze_match("Ajax vs Olympiacos", {"1X2_Home": 1.85})
        
        assert result["match"] == "Ajax vs Olympiacos"
        assert result["exp_goals_home"] == 1.8
        mock_post.assert_called_once()
    
    @patch('backend.services.llm_client.requests.post')
    def test_analyze_match_api_error(self, mock_post):
        """Verifica que los errores de API se manejan correctamente."""
        import requests
        mock_post.side_effect = requests.exceptions.RequestException("Connection failed")
        
        client = LLMAnalysisClient(api_key="test-key")
        
        with patch.object(client, '_get_system_prompt', return_value="Test system prompt"):
            result = client.analyze_match("Ajax vs Olympiacos", {"1X2_Home": 1.85})
        
        assert "error" in result
        assert "LLM API Error" in result["error"]
    
    @patch('backend.services.llm_client.requests.post')
    def test_analyze_match_timeout(self, mock_post):
        """Verifica que los timeouts se manejan correctamente."""
        import requests
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")
        
        client = LLMAnalysisClient(api_key="test-key")
        
        with patch.object(client, '_get_system_prompt', return_value="Test system prompt"):
            result = client.analyze_match("Ajax vs Olympiacos", {"1X2_Home": 1.85})
        
        assert "error" in result


class TestPrompts:
    """Tests para los prompts."""
    
    def test_system_prompt_exists(self):
        """Verifica que el SYSTEM_PROMPT existe y tiene contenido."""
        from backend.utils.prompts import SYSTEM_PROMPT
        
        assert SYSTEM_PROMPT is not None
        assert len(SYSTEM_PROMPT) > 100
        assert "Analista Profesional" in SYSTEM_PROMPT
        assert "Value Betting" in SYSTEM_PROMPT
        assert "JSON" in SYSTEM_PROMPT
    
    def test_analysis_prompt_template_exists(self):
        """Verifica que el template existe."""
        from backend.utils.prompts import ANALYSIS_PROMPT_TEMPLATE
        
        assert ANALYSIS_PROMPT_TEMPLATE is not None
        assert "{match_name}" in ANALYSIS_PROMPT_TEMPLATE
        assert "{odds}" in ANALYSIS_PROMPT_TEMPLATE


class TestConfig:
    """Tests para la configuración."""
    
    def test_config_defaults(self):
        """Verifica los valores por defecto de la configuración."""
        from backend import config
        
        # Solo verificamos que los valores existen (pueden ser overridden por env)
        assert hasattr(config, 'LLM_API_KEY')
        assert hasattr(config, 'LLM_BASE_URL')
        assert hasattr(config, 'BANKROLL')
        assert hasattr(config, 'KELLY_FRACTION')
    
    def test_config_types(self):
        """Verifica los tipos de datos de la configuración."""
        from backend import config
        
        assert isinstance(config.LLM_API_KEY, str)
        assert isinstance(config.LLM_BASE_URL, str)
        assert isinstance(config.BANKROLL, int)
        assert isinstance(config.KELLY_FRACTION, float)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
