from fastapi import APIRouter, HTTPException
from backend.models.analysis_models import AnalysisRequest, AnalysisResponse, BetRecommendation
from backend.services.llm_client import LLMAnalysisClient
from backend.services.analysis_engine import BettingEngine
from backend.config import LLM_API_KEY, BANKROLL, KELLY_FRACTION
from typing import Dict, List
import logging

router = APIRouter(prefix="/api", tags=["analysis"])
logger = logging.getLogger(__name__)

# Instanciar clientes
llm_client = LLMAnalysisClient(api_key=LLM_API_KEY)
betting_engine = BettingEngine(bankroll=BANKROLL, kelly_fraction=KELLY_FRACTION)

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_match(request: AnalysisRequest):
    """
    Endpoint principal de análisis.
    Orquesta: LLM → Motor Matemático → Respuesta formateada
    """
    try:
        # PASO 1: Obtener datos de la LLM (búsqueda web + parámetros λ)
        logger.info(f"Analizando: {request.match_name}")
        
        llm_response = llm_client.analyze_match(
            match_name=request.match_name,
            user_odds={
                "1": request.odds.home_win,
                "X": request.odds.draw,
                "2": request.odds.away_win,
                "over_2.5": request.odds.over_2_5,
                "btts": request.odds.btts_yes,
                "corners": request.odds.over_8_5_corners,
                "cards": request.odds.over_3_5_cards
            }
        )

        if "error" in llm_response:
            raise HTTPException(status_code=500, detail=llm_response["error"])

        # PASO 2: Extraer parámetros λ de la respuesta LLM
        exp_goals_home = llm_response.get("exp_goals_home", 1.5)
        exp_goals_away = llm_response.get("exp_goals_away", 1.0)
        exp_corners = llm_response.get("exp_corners", 9.0)
        exp_cards = llm_response.get("exp_cards", 4.0)
        key_insights = llm_response.get("key_insights", [])
        referee_info = llm_response.get("referee_info", "No disponible")

        # PASO 3: Calcular probabilidades con Poisson
        probs = betting_engine.get_poisson_probs(exp_goals_home, exp_goals_away)

        # PASO 4: Calcular cuotas justas
        fair_odds = {
            "1": 1 / probs["1"],
            "X": 1 / probs["X"],
            "2": 1 / probs["2"],
            "over_2.5": 1 / probs["over_2.5"],
            "btts": 1 / probs["btts_yes"]
        }

        # PASO 5: Calcular EV para cada mercado
        ev_analysis = {}
        if request.odds.home_win:
            ev_analysis["1"] = (probs["1"] * request.odds.home_win - 1) * 100
        if request.odds.draw:
            ev_analysis["X"] = (probs["X"] * request.odds.draw - 1) * 100
        if request.odds.away_win:
            ev_analysis["2"] = (probs["2"] * request.odds.away_win - 1) * 100
        if request.odds.over_2_5:
            ev_analysis["over_2.5"] = (probs["over_2.5"] * request.odds.over_2_5 - 1) * 100
        if request.odds.btts_yes:
            ev_analysis["btts"] = (probs["btts_yes"] * request.odds.btts_yes - 1) * 100

        # PASO 6: Identificar la mejor oportunidad (EV+ más alto)
        best_ev = None
        best_market = None
        best_selection = None
        best_odds = None
        best_prob = None

        for market, ev in ev_analysis.items():
            if ev > 0 and (best_ev is None or ev > best_ev):
                best_ev = ev
                best_market = market
                if market == "1":
                    best_selection = "Victoria Local"
                    best_odds = request.odds.home_win
                    best_prob = probs["1"]
                elif market == "X":
                    best_selection = "Empate"
                    best_odds = request.odds.draw
                    best_prob = probs["X"]
                elif market == "2":
                    best_selection = "Victoria Visitante"
                    best_odds = request.odds.away_win
                    best_prob = probs["2"]
                elif market == "over_2.5":
                    best_selection = "Más de 2.5 Goles"
                    best_odds = request.odds.over_2_5
                    best_prob = probs["over_2.5"]
                elif market == "btts":
                    best_selection = "Ambos Marcan"
                    best_odds = request.odds.btts_yes
                    best_prob = probs["btts_yes"]

        # PASO 7: Calcular stake sugerido (Kelly fraccional)
        if best_ev and best_odds and best_prob:
            stake = betting_engine.calculate_kelly_stake(best_prob, best_odds)
        else:
            stake = 0

        # PASO 8: Crear recomendación principal
        if best_ev and best_ev > 0:
            top_recommendation = BetRecommendation(
                market=best_market,
                selection=best_selection,
                odds=best_odds,
                prob_real=round(best_prob, 4),
                fair_odds=round(fair_odds.get(best_market, 0), 2),
                ev_percent=round(best_ev, 2),
                stake_suggested=stake,
                confidence=min(95, int(best_prob * 100)),
                reasoning=f"EV positivo del {best_ev:.1f}%. Probabilidad real: {best_prob*100:.1f}% vs cuota que implica {1/best_odds*100:.1f}%"
            )
        else:
            top_recommendation = BetRecommendation(
                market="NINGUNO",
                selection="Sin valor identificado",
                odds=0,
                prob_real=0,
                fair_odds=0,
                ev_percent=0,
                stake_suggested=0,
                confidence=0,
                reasoning="No hay oportunidades con EV+ en este partido"
            )

        # PASO 9: Otras oportunidades (EV+ secundarias)
        other_opportunities = []
        for market, ev in sorted(ev_analysis.items(), key=lambda x: x[1], reverse=True):
            if ev > 0 and ev != best_ev:
                if market == "1":
                    sel = "Victoria Local"
                    odds = request.odds.home_win
                    prob = probs["1"]
                elif market == "X":
                    sel = "Empate"
                    odds = request.odds.draw
                    prob = probs["X"]
                elif market == "2":
                    sel = "Victoria Visitante"
                    odds = request.odds.away_win
                    prob = probs["2"]
                elif market == "over_2.5":
                    sel = "Más de 2.5 Goles"
                    odds = request.odds.over_2_5
                    prob = probs["over_2.5"]
                elif market == "btts":
                    sel = "Ambos Marcan"
                    odds = request.odds.btts_yes
                    prob = probs["btts_yes"]
                else:
                    continue

                other_opportunities.append(BetRecommendation(
                    market=market,
                    selection=sel,
                    odds=odds,
                    prob_real=round(prob, 4),
                    fair_odds=round(1/prob, 2),
                    ev_percent=round(ev, 2),
                    stake_suggested=betting_engine.calculate_kelly_stake(prob, odds),
                    confidence=min(95, int(prob * 100)),
                    reasoning=f"EV: {ev:.1f}%"
                ))

        # PASO 10: Construir respuesta final
        response = AnalysisResponse(
            match_name=request.match_name,
            league="Champions League",  # Puedes extraer esto de la LLM
            date=None,
            exp_goals_home=round(exp_goals_home, 2),
            exp_goals_away=round(exp_goals_away, 2),
            exp_corners=round(exp_corners, 2),
            exp_cards=round(exp_cards, 2),
            prob_home_win=round(probs["1"], 4),
            prob_draw=round(probs["X"], 4),
            prob_away_win=round(probs["2"], 4),
            prob_over_2_5=round(probs["over_2.5"], 4),
            prob_under_2_5=round(1 - probs["over_2.5"], 4),
            prob_btts=round(probs["btts_yes"], 4),
            fair_odds_home=round(fair_odds["1"], 2),
            fair_odds_draw=round(fair_odds["X"], 2),
            fair_odds_away=round(fair_odds["2"], 2),
            fair_odds_over_2_5=round(fair_odds["over_2.5"], 2),
            fair_odds_btts=round(fair_odds["btts"], 2),
            ev_analysis=ev_analysis,
            top_recommendation=top_recommendation,
            other_opportunities=other_opportunities,
            key_insights=key_insights,
            referee_info=referee_info
        )

        logger.info(f"Análisis completado: {request.match_name}")
        return response

    except Exception as e:
        logger.error(f"Error en análisis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")

@router.get("/ping")
async def ping():
    """Health check"""
    return {"status": "ok", "message": "Backend is running"}
