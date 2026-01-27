"""
Funciones de formato para la aplicación de apuestas deportivas.
===============================================================
Utilidades para convertir y formatear probabilidades, cuotas y porcentajes.
"""

from typing import Optional


def prob_to_fair_odds(probability: float) -> float:
    """
    Convierte una probabilidad en cuota justa (fair odds).
    
    La cuota justa es el inverso de la probabilidad: odds = 1 / probability
    
    Args:
        probability: Probabilidad expresada como decimal (0-1)
        
    Returns:
        Cuota justa redondeada a 2 decimales. Retorna 0 si probability <= 0.
        
    Examples:
        >>> prob_to_fair_odds(0.5)
        2.0
        >>> prob_to_fair_odds(0.25)
        4.0
        >>> prob_to_fair_odds(0.333)
        3.0
    """
    if probability <= 0:
        return 0.0
    
    if probability >= 1:
        return 1.0
    
    return round(1 / probability, 2)


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Formatea un valor decimal como porcentaje.
    
    Args:
        value: Valor decimal a formatear (ej: 0.342)
        decimals: Número de decimales a mostrar (default 1)
        
    Returns:
        String formateado como porcentaje (ej: "34.2%")
        
    Examples:
        >>> format_percentage(0.342)
        '34.2%'
        >>> format_percentage(0.5)
        '50.0%'
        >>> format_percentage(0.12345, decimals=2)
        '12.35%'
    """
    percentage = value * 100
    return f"{percentage:.{decimals}f}%"


def format_odds(odds: float, decimals: int = 2) -> str:
    """
    Formatea cuotas con símbolo @.
    
    Args:
        odds: Cuota decimal a formatear
        decimals: Número de decimales (default 2)
        
    Returns:
        String formateado con @ (ej: "@2.50")
        
    Examples:
        >>> format_odds(2.5)
        '@2.50'
        >>> format_odds(1.8)
        '@1.80'
    """
    return f"@{odds:.{decimals}f}"


def format_ev(ev_percent: float) -> str:
    """
    Formatea Expected Value con indicador de signo y color.
    
    Args:
        ev_percent: EV como porcentaje (puede ser negativo)
        
    Returns:
        String formateado con signo (ej: "+5.2%" o "-3.1%")
        
    Examples:
        >>> format_ev(5.2)
        '+5.2%'
        >>> format_ev(-3.1)
        '-3.1%'
    """
    sign = "+" if ev_percent > 0 else ""
    return f"{sign}{ev_percent:.1f}%"


def format_stake(stake: float, currency: str = "€") -> str:
    """
    Formatea stake con símbolo de moneda.
    
    Args:
        stake: Cantidad a apostar
        currency: Símbolo de moneda (default "€")
        
    Returns:
        String formateado (ej: "€25.00")
        
    Examples:
        >>> format_stake(25.5)
        '€25.50'
        >>> format_stake(100, currency="$")
        '$100.00'
    """
    return f"{currency}{stake:.2f}"


def format_result(home_goals: int, away_goals: int) -> str:
    """
    Formatea un resultado de partido.
    
    Args:
        home_goals: Goles del equipo local
        away_goals: Goles del equipo visitante
        
    Returns:
        String con formato "X-Y"
        
    Examples:
        >>> format_result(2, 1)
        '2-1'
    """
    return f"{home_goals}-{away_goals}"


def odds_to_implied_prob(odds: float) -> float:
    """
    Convierte cuotas decimales a probabilidad implícita.
    
    Args:
        odds: Cuota decimal (ej: 2.50)
        
    Returns:
        Probabilidad implícita como decimal (0-1)
        
    Examples:
        >>> odds_to_implied_prob(2.0)
        0.5
        >>> odds_to_implied_prob(4.0)
        0.25
    """
    if odds <= 0:
        return 0.0
    return round(1 / odds, 4)


def calculate_overround(odds_list: list) -> float:
    """
    Calcula el margen/overround de un mercado.
    
    El overround es la suma de probabilidades implícitas - 1.
    Representa el margen del bookmaker.
    
    Args:
        odds_list: Lista de cuotas para un mercado (ej: [1.80, 3.50, 4.20] para 1X2)
        
    Returns:
        Overround como porcentaje (ej: 5.5 significa 5.5% de margen)
        
    Examples:
        >>> calculate_overround([1.80, 3.50, 4.20])  # Ejemplo 1X2
        8.65
    """
    if not odds_list or any(o <= 0 for o in odds_list):
        return 0.0
    
    total_implied = sum(1 / odds for odds in odds_list)
    overround = (total_implied - 1) * 100
    return round(overround, 2)


def format_market_name(market_key: str) -> str:
    """
    Convierte claves de mercado en nombres legibles.
    
    Args:
        market_key: Clave interna del mercado (ej: "over_2.5")
        
    Returns:
        Nombre legible (ej: "Over 2.5 Goles")
    """
    market_names = {
        "1": "Victoria Local",
        "X": "Empate",
        "2": "Victoria Visitante",
        "1X": "Local o Empate",
        "12": "Local o Visitante",
        "X2": "Empate o Visitante",
        "over_0.5": "Más de 0.5 Goles",
        "under_0.5": "Menos de 0.5 Goles",
        "over_1.5": "Más de 1.5 Goles",
        "under_1.5": "Menos de 1.5 Goles",
        "over_2.5": "Más de 2.5 Goles",
        "under_2.5": "Menos de 2.5 Goles",
        "over_3.5": "Más de 3.5 Goles",
        "under_3.5": "Menos de 3.5 Goles",
        "over_4.5": "Más de 4.5 Goles",
        "under_4.5": "Menos de 4.5 Goles",
        "over_5.5": "Más de 5.5 Goles",
        "under_5.5": "Menos de 5.5 Goles",
        "btts_yes": "Ambos Marcan - Sí",
        "btts_no": "Ambos Marcan - No",
    }
    
    return market_names.get(market_key, market_key.replace("_", " ").title())


def format_bet_summary(
    market: str,
    probability: float,
    odds: float,
    ev: float,
    stake: float,
    currency: str = "€"
) -> str:
    """
    Genera un resumen formateado de una apuesta.
    
    Args:
        market: Nombre del mercado
        probability: Probabilidad real
        odds: Cuota del bookmaker
        ev: Expected Value en porcentaje
        stake: Cantidad a apostar
        currency: Símbolo de moneda
        
    Returns:
        String con resumen completo de la apuesta
    """
    return (
        f"{format_market_name(market)}: "
        f"{format_percentage(probability)} | "
        f"{format_odds(odds)} | "
        f"EV: {format_ev(ev)} | "
        f"Stake: {format_stake(stake, currency)}"
    )
