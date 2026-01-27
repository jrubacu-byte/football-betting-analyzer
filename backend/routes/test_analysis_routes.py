import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Añadir el path del proyecto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.main import app

client = TestClient(app)


class TestPingEndpoint:
    """Tests para el endpoint /api/ping"""
    
    def test_ping_returns_ok(self):
        """Test que el endpoint ping responde correctamente"""
        response = client.get("/api/ping")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "message" in data


class TestAnalyzeEndpoint:
    """Tests para el endpoint /api/analyze"""
    
    @patch('backend.routes.analysis_routes.llm_client')
    def test_analyze_accepts_valid_request(self, mock_llm):
        """Test que el endpoint acepta peticiones válidas"""
        # Mock de la respuesta de LLM
        mock_llm.analyze_match.return_value = {
            "exp_goals_home": 1.8,
            "exp_goals_away": 1.2,
            "exp_corners": 10.5,
            "exp_cards": 4.0,
            "key_insights": ["Ajax en buena forma", "Olympiacos con bajas"],
            "referee_info": "Árbitro estricto"
        }
        
        request_data = {
            "match_name": "Ajax vs Olympiacos",
            "odds": {
                "home_win": 2.10,
                "draw": 3.40,
                "away_win": 3.50,
                "over_2_5": 1.85,
                "btts_yes": 1.70
            },
            "bankroll": 1000
        }
        
        response = client.post("/api/analyze", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        # Verificar estructura de respuesta
        assert "match_name" in data
        assert "exp_goals_home" in data
        assert "exp_goals_away" in data
        assert "prob_home_win" in data
        assert "prob_draw" in data
        assert "prob_away_win" in data
        assert "ev_analysis" in data
        assert "top_recommendation" in data
        assert "other_opportunities" in data
        assert "key_insights" in data
    
    def test_analyze_rejects_invalid_request_missing_odds(self):
        """Test que rechaza peticiones sin odds"""
        request_data = {
            "match_name": "Ajax vs Olympiacos"
        }
        
        response = client.post("/api/analyze", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_analyze_rejects_invalid_request_missing_match_name(self):
        """Test que rechaza peticiones sin match_name"""
        request_data = {
            "odds": {
                "home_win": 2.10,
                "draw": 3.40,
                "away_win": 3.50
            }
        }
        
        response = client.post("/api/analyze", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_analyze_rejects_incomplete_odds(self):
        """Test que rechaza peticiones con odds incompletos (falta home_win, draw o away_win)"""
        request_data = {
            "match_name": "Ajax vs Olympiacos",
            "odds": {
                "home_win": 2.10
                # Faltan draw y away_win que son requeridos
            }
        }
        
        response = client.post("/api/analyze", json=request_data)
        assert response.status_code == 422  # Validation error
    
    @patch('backend.routes.analysis_routes.llm_client')
    def test_analyze_response_has_correct_structure(self, mock_llm):
        """Test que la respuesta tiene la estructura correcta"""
        mock_llm.analyze_match.return_value = {
            "exp_goals_home": 2.0,
            "exp_goals_away": 0.8,
            "exp_corners": 9.5,
            "exp_cards": 3.5,
            "key_insights": ["Equipo local muy ofensivo"],
            "referee_info": "Árbitro permisivo"
        }
        
        request_data = {
            "match_name": "Barcelona vs Real Madrid",
            "odds": {
                "home_win": 1.80,
                "draw": 3.60,
                "away_win": 4.20,
                "over_2_5": 1.75,
                "btts_yes": 1.80
            },
            "bankroll": 500
        }
        
        response = client.post("/api/analyze", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        # Verificar campos de probabilidades
        assert 0 <= data["prob_home_win"] <= 1
        assert 0 <= data["prob_draw"] <= 1
        assert 0 <= data["prob_away_win"] <= 1
        assert 0 <= data["prob_over_2_5"] <= 1
        assert 0 <= data["prob_btts"] <= 1
        
        # Verificar que las probabilidades 1X2 suman ~1
        total_1x2 = data["prob_home_win"] + data["prob_draw"] + data["prob_away_win"]
        assert 0.99 <= total_1x2 <= 1.01
        
        # Verificar estructura de top_recommendation
        rec = data["top_recommendation"]
        assert "market" in rec
        assert "selection" in rec
        assert "odds" in rec
        assert "prob_real" in rec
        assert "ev_percent" in rec
        assert "stake_suggested" in rec
        assert "confidence" in rec
        assert "reasoning" in rec
    
    @patch('backend.routes.analysis_routes.llm_client')
    def test_analyze_handles_llm_error(self, mock_llm):
        """Test que maneja errores de LLM correctamente"""
        mock_llm.analyze_match.return_value = {
            "error": "API connection failed"
        }
        
        request_data = {
            "match_name": "Ajax vs Olympiacos",
            "odds": {
                "home_win": 2.10,
                "draw": 3.40,
                "away_win": 3.50
            }
        }
        
        response = client.post("/api/analyze", json=request_data)
        assert response.status_code == 500
    
    @patch('backend.routes.analysis_routes.llm_client')
    def test_analyze_with_optional_odds(self, mock_llm):
        """Test que funciona con solo odds requeridos (sin over_2_5, btts, etc.)"""
        mock_llm.analyze_match.return_value = {
            "exp_goals_home": 1.5,
            "exp_goals_away": 1.0,
            "exp_corners": 9.0,
            "exp_cards": 4.0,
            "key_insights": [],
            "referee_info": "No disponible"
        }
        
        request_data = {
            "match_name": "Team A vs Team B",
            "odds": {
                "home_win": 2.00,
                "draw": 3.50,
                "away_win": 3.80
            }
        }
        
        response = client.post("/api/analyze", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        # Verificar que el análisis se completó
        assert data["match_name"] == "Team A vs Team B"
        assert "ev_analysis" in data
        # Solo deberían estar los EVs de 1, X, 2
        assert "1" in data["ev_analysis"]
        assert "X" in data["ev_analysis"]
        assert "2" in data["ev_analysis"]


class TestDataValidation:
    """Tests para validación de datos"""
    
    def test_odds_must_be_positive(self):
        """Test que las cuotas deben ser positivas"""
        request_data = {
            "match_name": "Ajax vs Olympiacos",
            "odds": {
                "home_win": -2.10,  # Negativo - inválido
                "draw": 3.40,
                "away_win": 3.50
            }
        }
        
        # El modelo Pydantic actual no valida que sean positivos,
        # pero el cálculo de probabilidades fallará con valores negativos
        # Este test documenta el comportamiento actual
        response = client.post("/api/analyze", json=request_data)
        # Debería devolver error porque no se puede calcular con odds negativos
        assert response.status_code in [422, 500]
    
    def test_bankroll_default_value(self):
        """Test que el bankroll tiene un valor por defecto de 1000"""
        from backend.models.analysis_models import AnalysisRequest, OddsInput
        
        odds = OddsInput(home_win=2.0, draw=3.0, away_win=4.0)
        request = AnalysisRequest(match_name="Test Match", odds=odds)
        
        assert request.bankroll == 1000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
