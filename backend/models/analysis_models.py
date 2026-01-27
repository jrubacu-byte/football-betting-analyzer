from pydantic import BaseModel
from typing import Dict, List, Optional

class OddsInput(BaseModel):
    """Modelo para las cuotas del bookmaker"""
    home_win: float  # Cuota para victoria local (1)
    draw: float      # Cuota para empate (X)
    away_win: float  # Cuota para victoria visitante (2)
    over_2_5: Optional[float] = None  # Cuota para Más de 2.5 goles
    under_2_5: Optional[float] = None  # Cuota para Menos de 2.5 goles
    btts_yes: Optional[float] = None  # Cuota para Ambos Marcan
    over_8_5_corners: Optional[float] = None  # Cuota para Más de 8.5 córners
    over_3_5_cards: Optional[float] = None  # Cuota para Más de 3.5 tarjetas

class AnalysisRequest(BaseModel):
    """Modelo para la petición de análisis"""
    match_name: str  # Ej: "Ajax vs Olympiacos"
    odds: OddsInput
    bankroll: Optional[float] = 1000

class BetRecommendation(BaseModel):
    """Modelo para la apuesta recomendada"""
    market: str
    selection: str
    odds: float
    prob_real: float
    fair_odds: float
    ev_percent: float
    stake_suggested: float
    confidence: int
    reasoning: str

class AnalysisResponse(BaseModel):
    """Modelo para la respuesta completa del análisis"""
    match_name: str
    league: Optional[str]
    date: Optional[str]
    
    # Parámetros del modelo
    exp_goals_home: float
    exp_goals_away: float
    exp_corners: float
    exp_cards: float
    
    # Probabilidades 1X2
    prob_home_win: float
    prob_draw: float
    prob_away_win: float
    
    # Probabilidades de goles
    prob_over_2_5: float
    prob_under_2_5: float
    prob_btts: float
    
    # Cuotas justas
    fair_odds_home: float
    fair_odds_draw: float
    fair_odds_away: float
    fair_odds_over_2_5: float
    fair_odds_btts: float
    
    # Análisis de valor
    ev_analysis: Dict[str, float]  # {"1": 5.2, "X": -2.1, "2": 3.8, ...}
    
    # Recomendación principal
    top_recommendation: BetRecommendation
    
    # Otras oportunidades
    other_opportunities: List[BetRecommendation]
    
    # Contexto
    key_insights: List[str]
    referee_info: str
