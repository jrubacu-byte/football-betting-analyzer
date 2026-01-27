"""
Motor de Análisis Estadístico para Apuestas Deportivas
=======================================================
Implementa cálculos de probabilidades usando distribución Poisson,
Expected Value y gestión de stake con Kelly Criterion.
"""

import numpy as np
from scipy.stats import poisson
from typing import Dict, List, Tuple, Optional


class BettingEngine:
    """
    Motor matemático para cálculos de apuestas deportivas.
    
    Attributes:
        bankroll: Capital inicial para gestión de stakes
        kelly_fraction: Fracción del Kelly Criterion a usar (default 0.25 = 25%)
    """
    
    def __init__(self, bankroll: float = 1000, kelly_fraction: float = 0.25):
        """
        Inicializa el motor de apuestas.
        
        Args:
            bankroll: Capital inicial (default 1000)
            kelly_fraction: Fracción de Kelly a usar, típicamente 0.25 para ser conservador
        """
        self.bankroll = bankroll
        self.kelly_fraction = kelly_fraction
    
    def calculate_poisson_matrix(self, exp_goals_home: float, exp_goals_away: float) -> np.ndarray:
        """
        Genera matriz 8x8 de probabilidades de resultados exactos usando distribución Poisson.
        
        Args:
            exp_goals_home: Goles esperados del equipo local
            exp_goals_away: Goles esperados del equipo visitante
            
        Returns:
            Matriz numpy 8x8 donde matrix[i][j] = P(Home=i, Away=j)
        """
        max_goals = 8
        home_probs = poisson.pmf(range(max_goals), exp_goals_home)
        away_probs = poisson.pmf(range(max_goals), exp_goals_away)
        matrix = np.outer(home_probs, away_probs)
        return matrix
    
    def get_market_probs(self, matrix: np.ndarray) -> Dict[str, float]:
        """
        Calcula probabilidades para todos los mercados a partir de la matriz Poisson.
        
        Args:
            matrix: Matriz de probabilidades de resultados exactos
            
        Returns:
            Diccionario con probabilidades para cada mercado
        """
        probs = {}
        
        # === Mercado 1X2 ===
        # Victoria local (1): goles home > goles away - triángulo inferior
        probs["1"] = float(np.sum(np.tril(matrix, -1)))
        # Empate (X): diagonal principal
        probs["X"] = float(np.sum(np.diag(matrix)))
        # Victoria visitante (2): goles away > goles home - triángulo superior
        probs["2"] = float(np.sum(np.triu(matrix, 1)))
        
        # === Mercados de Goles ===
        # Calculamos sumas acumuladas para diferentes líneas
        total_goals_probs = {}
        for total in range(16):  # 0 a 15 goles totales
            prob = sum(matrix[i, j] for i in range(8) for j in range(8) if i + j == total)
            total_goals_probs[total] = prob
        
        # Over/Under 0.5
        probs["under_0.5"] = float(matrix[0, 0])
        probs["over_0.5"] = float(1 - matrix[0, 0])
        
        # Over/Under 1.5
        under_1_5 = sum(total_goals_probs[g] for g in range(2))  # 0, 1 goles
        probs["under_1.5"] = float(under_1_5)
        probs["over_1.5"] = float(1 - under_1_5)
        
        # Over/Under 2.5
        under_2_5 = sum(total_goals_probs[g] for g in range(3))  # 0, 1, 2 goles
        probs["under_2.5"] = float(under_2_5)
        probs["over_2.5"] = float(1 - under_2_5)
        
        # Over/Under 3.5
        under_3_5 = sum(total_goals_probs[g] for g in range(4))  # 0, 1, 2, 3 goles
        probs["under_3.5"] = float(under_3_5)
        probs["over_3.5"] = float(1 - under_3_5)
        
        # Over/Under 4.5
        under_4_5 = sum(total_goals_probs[g] for g in range(5))
        probs["under_4.5"] = float(under_4_5)
        probs["over_4.5"] = float(1 - under_4_5)
        
        # Over/Under 5.5
        under_5_5 = sum(total_goals_probs[g] for g in range(6))
        probs["under_5.5"] = float(under_5_5)
        probs["over_5.5"] = float(1 - under_5_5)
        
        # === BTTS (Both Teams To Score) ===
        # Ambos equipos marcan: excluir filas donde home=0 y columnas donde away=0
        no_btts = matrix[0, :].sum() + matrix[:, 0].sum() - matrix[0, 0]
        probs["btts_yes"] = float(1 - no_btts)
        probs["btts_no"] = float(no_btts)
        
        # === Doble Oportunidad ===
        probs["1X"] = probs["1"] + probs["X"]  # Local o empate
        probs["12"] = probs["1"] + probs["2"]  # Local o visitante (no empate)
        probs["X2"] = probs["X"] + probs["2"]  # Empate o visitante
        
        # === Goles Exactos ===
        for goals in range(6):
            probs[f"exact_{goals}_goals"] = float(total_goals_probs.get(goals, 0))
        probs["exact_6+_goals"] = float(1 - sum(total_goals_probs.get(g, 0) for g in range(6)))
        
        return probs
    
    def get_poisson_probs(self, home_exp: float, away_exp: float) -> Dict[str, float]:
        """
        Método integrado: calcula matriz y extrae probabilidades de mercados.
        
        Args:
            home_exp: Goles esperados del equipo local
            away_exp: Goles esperados del equipo visitante
            
        Returns:
            Diccionario con todas las probabilidades de mercados
        """
        matrix = self.calculate_poisson_matrix(home_exp, away_exp)
        probs = self.get_market_probs(matrix)
        probs["_matrix"] = matrix  # Incluir matriz para análisis adicional
        return probs
    
    def calculate_ev_and_stake(
        self, 
        prob_real: float, 
        odds_bookie: float, 
        bankroll: Optional[float] = None
    ) -> Tuple[float, float]:
        """
        Calcula Expected Value y stake sugerido usando Kelly Fraccional.
        
        Args:
            prob_real: Probabilidad real estimada (0-1)
            odds_bookie: Cuota ofrecida por la casa de apuestas
            bankroll: Capital a usar (default: self.bankroll)
            
        Returns:
            Tupla (ev_percent, stake_suggested)
            - ev_percent: Expected Value como porcentaje
            - stake_suggested: Cantidad sugerida a apostar
        """
        if bankroll is None:
            bankroll = self.bankroll
        
        # Expected Value: EV = (prob_real × odds_bookie) - 1
        ev = (prob_real * odds_bookie) - 1
        ev_percent = ev * 100  # Convertir a porcentaje
        
        # Kelly Criterion: k = (prob × b - (1 - prob)) / b, donde b = odds - 1
        b = odds_bookie - 1
        
        if b <= 0 or prob_real <= 0 or prob_real >= 1:
            return (ev_percent, 0.0)
        
        kelly = (prob_real * b - (1 - prob_real)) / b
        
        # Solo apostar si Kelly es positivo (EV > 0)
        if kelly <= 0:
            return (ev_percent, 0.0)
        
        # Stake = k × kelly_fraction × bankroll
        stake = kelly * self.kelly_fraction * bankroll
        stake_suggested = round(max(0, stake), 2)
        
        return (round(ev_percent, 2), stake_suggested)
    
    def calculate_kelly_stake(self, prob: float, odds: float) -> float:
        """
        Calcula stake usando Kelly Criterion fraccional.
        
        Args:
            prob: Probabilidad real estimada (0-1)
            odds: Cuota decimal
            
        Returns:
            Stake sugerido en unidades monetarias
        """
        if prob <= 0 or prob >= 1 or odds <= 1:
            return 0.0
            
        if prob * odds <= 1:  # No hay valor positivo
            return 0.0
            
        b = odds - 1
        k = (prob * b - (1 - prob)) / b
        
        if k <= 0:
            return 0.0
            
        return round(k * self.kelly_fraction * self.bankroll, 2)
    
    def estimate_corners_and_cards(
        self, 
        avg_corners_home: float, 
        avg_corners_away: float,
        avg_cards_home: float = 2.0,
        avg_cards_away: float = 2.0,
        referee_factor: float = 1.0
    ) -> Dict[str, Dict[str, float]]:
        """
        Calcula probabilidades para mercados de córners y tarjetas.
        
        Args:
            avg_corners_home: Promedio de córners del equipo local
            avg_corners_away: Promedio de córners del equipo visitante
            avg_cards_home: Promedio de tarjetas del equipo local (default 2.0)
            avg_cards_away: Promedio de tarjetas del equipo visitante (default 2.0)
            referee_factor: Factor de ajuste para árbitro (>1 = más tarjetas)
            
        Returns:
            Diccionario con probabilidades de córners y tarjetas
        """
        result = {
            "corners": {},
            "cards": {}
        }
        
        # === Mercados de Córners ===
        total_corners_exp = avg_corners_home + avg_corners_away
        
        # Calculamos probabilidades acumuladas usando Poisson
        corners_probs = {}
        for n in range(25):  # 0 a 24 córners
            corners_probs[n] = poisson.pmf(n, total_corners_exp)
        
        # Over/Under 7.5 córners
        under_7_5 = sum(corners_probs[n] for n in range(8))
        result["corners"]["under_7.5"] = float(under_7_5)
        result["corners"]["over_7.5"] = float(1 - under_7_5)
        
        # Over/Under 8.5 córners
        under_8_5 = sum(corners_probs[n] for n in range(9))
        result["corners"]["under_8.5"] = float(under_8_5)
        result["corners"]["over_8.5"] = float(1 - under_8_5)
        
        # Over/Under 9.5 córners
        under_9_5 = sum(corners_probs[n] for n in range(10))
        result["corners"]["under_9.5"] = float(under_9_5)
        result["corners"]["over_9.5"] = float(1 - under_9_5)
        
        # Over/Under 10.5 córners
        under_10_5 = sum(corners_probs[n] for n in range(11))
        result["corners"]["under_10.5"] = float(under_10_5)
        result["corners"]["over_10.5"] = float(1 - under_10_5)
        
        # Over/Under 11.5 córners
        under_11_5 = sum(corners_probs[n] for n in range(12))
        result["corners"]["under_11.5"] = float(under_11_5)
        result["corners"]["over_11.5"] = float(1 - under_11_5)
        
        # Over/Under 12.5 córners
        under_12_5 = sum(corners_probs[n] for n in range(13))
        result["corners"]["under_12.5"] = float(under_12_5)
        result["corners"]["over_12.5"] = float(1 - under_12_5)
        
        # Córners exactos
        result["corners"]["expected"] = float(total_corners_exp)
        
        # === Mercados de Tarjetas ===
        # Aplicar factor del árbitro
        total_cards_exp = (avg_cards_home + avg_cards_away) * referee_factor
        
        cards_probs = {}
        for n in range(20):  # 0 a 19 tarjetas
            cards_probs[n] = poisson.pmf(n, total_cards_exp)
        
        # Over/Under 2.5 tarjetas
        under_2_5 = sum(cards_probs[n] for n in range(3))
        result["cards"]["under_2.5"] = float(under_2_5)
        result["cards"]["over_2.5"] = float(1 - under_2_5)
        
        # Over/Under 3.5 tarjetas
        under_3_5 = sum(cards_probs[n] for n in range(4))
        result["cards"]["under_3.5"] = float(under_3_5)
        result["cards"]["over_3.5"] = float(1 - under_3_5)
        
        # Over/Under 4.5 tarjetas
        under_4_5 = sum(cards_probs[n] for n in range(5))
        result["cards"]["under_4.5"] = float(under_4_5)
        result["cards"]["over_4.5"] = float(1 - under_4_5)
        
        # Over/Under 5.5 tarjetas
        under_5_5 = sum(cards_probs[n] for n in range(6))
        result["cards"]["under_5.5"] = float(under_5_5)
        result["cards"]["over_5.5"] = float(1 - under_5_5)
        
        # Over/Under 6.5 tarjetas
        under_6_5 = sum(cards_probs[n] for n in range(7))
        result["cards"]["under_6.5"] = float(under_6_5)
        result["cards"]["over_6.5"] = float(1 - under_6_5)
        
        # Tarjetas esperadas
        result["cards"]["expected"] = float(total_cards_exp)
        
        return result
    
    def get_top_results(self, matrix: np.ndarray, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Extrae los top N resultados más probables de la matriz.
        
        Args:
            matrix: Matriz de probabilidades de resultados exactos
            top_n: Número de resultados a retornar (default 10)
            
        Returns:
            Lista de tuplas (resultado, probabilidad) ordenadas de mayor a menor
        """
        results = []
        rows, cols = matrix.shape
        
        for i in range(rows):
            for j in range(cols):
                prob = float(matrix[i, j])
                if prob > 0:
                    result_str = f"{i}-{j}"
                    results.append((result_str, prob))
        
        # Ordenar por probabilidad descendente
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:top_n]
    
    def analyze_match(
        self, 
        home_exp_goals: float,
        away_exp_goals: float,
        avg_corners_home: float = 5.0,
        avg_corners_away: float = 4.5,
        avg_cards_home: float = 2.0,
        avg_cards_away: float = 2.0,
        referee_factor: float = 1.0
    ) -> Dict:
        """
        Análisis completo de un partido: goles, córners y tarjetas.
        
        Args:
            home_exp_goals: Goles esperados del equipo local
            away_exp_goals: Goles esperados del equipo visitante
            avg_corners_home: Promedio de córners del local
            avg_corners_away: Promedio de córners del visitante
            avg_cards_home: Promedio de tarjetas del local
            avg_cards_away: Promedio de tarjetas del visitante
            referee_factor: Factor de ajuste del árbitro
            
        Returns:
            Diccionario completo con todas las probabilidades
        """
        # Matriz y probabilidades de goles
        matrix = self.calculate_poisson_matrix(home_exp_goals, away_exp_goals)
        goals_probs = self.get_market_probs(matrix)
        
        # Remover la matriz del diccionario de probabilidades
        if "_matrix" in goals_probs:
            del goals_probs["_matrix"]
        
        # Probabilidades de córners y tarjetas
        secondary = self.estimate_corners_and_cards(
            avg_corners_home, 
            avg_corners_away,
            avg_cards_home,
            avg_cards_away,
            referee_factor
        )
        
        # Top resultados más probables
        top_results = self.get_top_results(matrix, top_n=10)
        
        return {
            "goals": goals_probs,
            "corners": secondary["corners"],
            "cards": secondary["cards"],
            "top_results": top_results,
            "expected_goals": {
                "home": home_exp_goals,
                "away": away_exp_goals,
                "total": home_exp_goals + away_exp_goals
            }
        }
    
    def find_value_bets(
        self, 
        probs: Dict[str, float], 
        bookmaker_odds: Dict[str, float],
        min_ev_threshold: float = 0.0
    ) -> List[Dict]:
        """
        Encuentra apuestas con valor positivo comparando probabilidades con cuotas.
        
        Args:
            probs: Diccionario con probabilidades calculadas
            bookmaker_odds: Diccionario con cuotas del bookmaker
            min_ev_threshold: EV mínimo para considerar (default 0%)
            
        Returns:
            Lista de apuestas con valor ordenadas por EV
        """
        value_bets = []
        
        for market, prob in probs.items():
            if market.startswith("_"):  # Ignorar campos internos
                continue
                
            if market in bookmaker_odds:
                odds = bookmaker_odds[market]
                ev_percent, stake = self.calculate_ev_and_stake(prob, odds)
                
                if ev_percent > min_ev_threshold:
                    fair_odds = round(1 / prob, 2) if prob > 0 else 0
                    value_bets.append({
                        "market": market,
                        "probability": round(prob * 100, 2),
                        "fair_odds": fair_odds,
                        "bookmaker_odds": odds,
                        "ev_percent": ev_percent,
                        "suggested_stake": stake,
                        "edge": round((1 / fair_odds - 1 / odds) * 100, 2) if fair_odds > 0 else 0
                    })
        
        # Ordenar por EV descendente
        value_bets.sort(key=lambda x: x["ev_percent"], reverse=True)
        
        return value_bets
