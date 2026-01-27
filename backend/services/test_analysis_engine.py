"""
Tests para el Motor de Análisis Estadístico
============================================
Verifica el correcto funcionamiento de los cálculos de probabilidades,
EV y stakes usando pytest.
"""

import pytest
import numpy as np
import sys
import os

# Añadir el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.analysis_engine import BettingEngine
from utils.formatters import prob_to_fair_odds, format_percentage, format_odds


class TestPoissonMatrix:
    """Tests para la matriz de Poisson"""
    
    def setup_method(self):
        """Inicializa el engine para cada test"""
        self.engine = BettingEngine(bankroll=1000, kelly_fraction=0.25)
    
    def test_matrix_shape(self):
        """La matriz debe ser 8x8"""
        matrix = self.engine.calculate_poisson_matrix(1.5, 1.2)
        assert matrix.shape == (8, 8)
    
    def test_matrix_sums_to_approximately_one(self):
        """La matriz debe sumar aproximadamente 1.0 (puede haber pequeña pérdida por truncamiento)"""
        matrix = self.engine.calculate_poisson_matrix(1.5, 1.2)
        total = np.sum(matrix)
        # Debe ser muy cercano a 1 (al menos 0.99 debido a truncamiento en 8 goles)
        assert 0.99 < total <= 1.0, f"La matriz suma {total}, debería ser ~1.0"
    
    def test_matrix_all_positive(self):
        """Todas las probabilidades deben ser positivas"""
        matrix = self.engine.calculate_poisson_matrix(2.0, 1.5)
        assert np.all(matrix >= 0)
    
    def test_matrix_with_different_expectations(self):
        """Probar con diferentes expectativas de goles"""
        for home_exp in [0.5, 1.0, 2.0, 3.0]:
            for away_exp in [0.5, 1.0, 2.0, 3.0]:
                matrix = self.engine.calculate_poisson_matrix(home_exp, away_exp)
                assert matrix.shape == (8, 8)
                assert np.all(matrix >= 0)


class TestMarketProbabilities:
    """Tests para probabilidades de mercados"""
    
    def setup_method(self):
        self.engine = BettingEngine()
    
    def test_1x2_sums_to_one(self):
        """Las probabilidades 1X2 deben sumar 1.0"""
        probs = self.engine.get_poisson_probs(1.5, 1.2)
        total_1x2 = probs["1"] + probs["X"] + probs["2"]
        assert abs(total_1x2 - 1.0) < 0.02, f"1X2 suma {total_1x2}, debería ser 1.0"
    
    def test_over_under_are_complementary(self):
        """Over y Under deben ser complementarios"""
        probs = self.engine.get_poisson_probs(1.5, 1.2)
        
        # Over 2.5 + Under 2.5 = 1
        assert abs(probs["over_2.5"] + probs["under_2.5"] - 1.0) < 0.01
        
        # Over 1.5 + Under 1.5 = 1
        assert abs(probs["over_1.5"] + probs["under_1.5"] - 1.0) < 0.01
        
        # Over 3.5 + Under 3.5 = 1
        assert abs(probs["over_3.5"] + probs["under_3.5"] - 1.0) < 0.01
    
    def test_btts_are_complementary(self):
        """BTTS Sí y No deben sumar 1.0"""
        probs = self.engine.get_poisson_probs(1.5, 1.2)
        total_btts = probs["btts_yes"] + probs["btts_no"]
        assert abs(total_btts - 1.0) < 0.01
    
    def test_double_chance_probabilities(self):
        """Las probabilidades de doble oportunidad son correctas"""
        probs = self.engine.get_poisson_probs(1.5, 1.2)
        
        # 1X = 1 + X
        assert abs(probs["1X"] - (probs["1"] + probs["X"])) < 0.001
        
        # X2 = X + 2
        assert abs(probs["X2"] - (probs["X"] + probs["2"])) < 0.001


class TestKellyStake:
    """Tests para cálculos de Kelly Criterion"""
    
    def setup_method(self):
        self.engine = BettingEngine(bankroll=1000, kelly_fraction=0.25)
    
    def test_kelly_positive_ev(self):
        """Kelly debe retornar stake positivo cuando hay valor"""
        # prob=0.5, odds=2.5 -> hay valor positivo
        stake = self.engine.calculate_kelly_stake(0.5, 2.5)
        assert stake > 0
    
    def test_kelly_negative_ev(self):
        """Kelly debe retornar 0 cuando no hay valor"""
        # prob=0.3, odds=2.0 -> no hay valor (0.3*2.0 = 0.6 < 1)
        stake = self.engine.calculate_kelly_stake(0.3, 2.0)
        assert stake == 0
    
    def test_kelly_edge_cases(self):
        """Kelly maneja casos límite correctamente"""
        assert self.engine.calculate_kelly_stake(0, 2.0) == 0
        assert self.engine.calculate_kelly_stake(1.0, 2.0) == 0
        assert self.engine.calculate_kelly_stake(0.5, 1.0) == 0
    
    def test_calculate_ev_and_stake(self):
        """Prueba del cálculo de EV y stake combinado"""
        ev, stake = self.engine.calculate_ev_and_stake(0.5, 2.5, 1000)
        
        # EV = (0.5 * 2.5) - 1 = 0.25 = 25%
        assert abs(ev - 25.0) < 0.1
        assert stake > 0


class TestCornersAndCards:
    """Tests para mercados de córners y tarjetas"""
    
    def setup_method(self):
        self.engine = BettingEngine()
    
    def test_corners_probabilities(self):
        """Las probabilidades de córners son válidas"""
        result = self.engine.estimate_corners_and_cards(
            avg_corners_home=5.5,
            avg_corners_away=4.5,
            avg_cards_home=2.0,
            avg_cards_away=2.0
        )
        
        # Over + Under 9.5 = 1
        corners = result["corners"]
        assert abs(corners["over_9.5"] + corners["under_9.5"] - 1.0) < 0.01
        
        # Todas las probabilidades entre 0 y 1
        for key, value in corners.items():
            if key != "expected":
                assert 0 <= value <= 1, f"Probabilidad inválida para {key}: {value}"
    
    def test_cards_with_referee_factor(self):
        """El factor del árbitro afecta las probabilidades de tarjetas"""
        result_normal = self.engine.estimate_corners_and_cards(
            avg_corners_home=5.0, avg_corners_away=4.5,
            avg_cards_home=2.0, avg_cards_away=2.0,
            referee_factor=1.0
        )
        
        result_strict = self.engine.estimate_corners_and_cards(
            avg_corners_home=5.0, avg_corners_away=4.5,
            avg_cards_home=2.0, avg_cards_away=2.0,
            referee_factor=1.5  # Árbitro más estricto
        )
        
        # Con árbitro estricto, over debe ser más probable
        assert result_strict["cards"]["over_4.5"] > result_normal["cards"]["over_4.5"]


class TestTopResults:
    """Tests para la extracción de resultados más probables"""
    
    def setup_method(self):
        self.engine = BettingEngine()
    
    def test_top_results_count(self):
        """Debe retornar el número correcto de resultados"""
        matrix = self.engine.calculate_poisson_matrix(1.5, 1.2)
        
        top_5 = self.engine.get_top_results(matrix, top_n=5)
        assert len(top_5) == 5
        
        top_10 = self.engine.get_top_results(matrix, top_n=10)
        assert len(top_10) == 10
    
    def test_top_results_sorted(self):
        """Los resultados deben estar ordenados por probabilidad"""
        matrix = self.engine.calculate_poisson_matrix(1.5, 1.2)
        top_results = self.engine.get_top_results(matrix, top_n=10)
        
        # Verificar orden descendente
        probs = [r[1] for r in top_results]
        assert probs == sorted(probs, reverse=True)


class TestFormatters:
    """Tests para las funciones de formato"""
    
    def test_prob_to_fair_odds(self):
        """Conversión de probabilidad a cuota justa"""
        assert prob_to_fair_odds(0.5) == 2.0
        assert prob_to_fair_odds(0.25) == 4.0
        assert prob_to_fair_odds(0.0) == 0.0  # Caso límite
        assert prob_to_fair_odds(1.0) == 1.0  # Caso límite
    
    def test_format_percentage(self):
        """Formato de porcentajes"""
        assert format_percentage(0.5) == "50.0%"
        assert format_percentage(0.342) == "34.2%"
        assert format_percentage(0.12345, decimals=2) == "12.35%"
    
    def test_format_odds(self):
        """Formato de cuotas"""
        assert format_odds(2.5) == "@2.50"
        assert format_odds(1.8) == "@1.80"


class TestMatchAnalysis:
    """Tests para el análisis completo de partidos"""
    
    def setup_method(self):
        self.engine = BettingEngine(bankroll=1000, kelly_fraction=0.25)
    
    def test_analyze_match_returns_all_markets(self):
        """El análisis debe incluir todos los mercados"""
        result = self.engine.analyze_match(
            home_exp_goals=1.5,
            away_exp_goals=1.2
        )
        
        assert "goals" in result
        assert "corners" in result
        assert "cards" in result
        assert "top_results" in result
        assert "expected_goals" in result
        
        # Verificar mercados de goles
        assert "1" in result["goals"]
        assert "X" in result["goals"]
        assert "2" in result["goals"]
        assert "over_2.5" in result["goals"]
        assert "btts_yes" in result["goals"]
    
    def test_find_value_bets(self):
        """Encuentra apuestas con valor positivo"""
        probs = self.engine.get_poisson_probs(1.5, 1.0)
        
        # Cuotas que generan valor positivo
        bookmaker_odds = {
            "1": 2.5,  # Si prob > 0.4, hay valor
            "X": 4.0,
            "2": 3.5,
            "over_2.5": 2.0
        }
        
        value_bets = self.engine.find_value_bets(probs, bookmaker_odds)
        
        # Debe retornar una lista
        assert isinstance(value_bets, list)
        
        # Si hay apuestas con valor, deben tener EV positivo
        for bet in value_bets:
            assert bet["ev_percent"] > 0
            assert "market" in bet
            assert "suggested_stake" in bet


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
