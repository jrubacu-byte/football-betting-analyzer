export const formatOdds = (odds: number): string => {
  if (odds == null || isNaN(odds)) return '-';
  return odds.toFixed(2);
};

export const formatPercentage = (value: number): string => {
  if (value == null || isNaN(value)) return '-';
  return `${value.toFixed(1)}%`;
};

export const formatEV = (ev: number): { text: string; color: string } => {
  if (ev == null || isNaN(ev)) {
    return { text: '-', color: '#95a5a6' };
  }
  
  const sign = ev >= 0 ? '+' : '';
  const color = getConfidenceColor(ev);
  
  return {
    text: `${sign}${ev.toFixed(1)}%`,
    color,
  };
};

export const formatStake = (stake: number): string => {
  if (stake == null || isNaN(stake)) return '-';
  return `${stake.toFixed(2)}€`;
};

export const getConfidenceColor = (ev: number): string => {
  if (ev == null || isNaN(ev)) return '#95a5a6';
  
  if (ev >= 5) return '#27ae60'; // Green for high EV
  if (ev >= 3) return '#3498db'; // Blue for medium EV
  if (ev >= 0) return '#95a5a6'; // Gray for low positive EV
  return '#e74c3c'; // Red for negative EV
};

export const formatDate = (timestamp: string): string => {
  try {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Hace un momento';
    if (diffMins < 60) return `Hace ${diffMins} min`;
    if (diffHours < 24) return `Hace ${diffHours} h`;
    if (diffDays < 7) return `Hace ${diffDays} días`;
    
    return date.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    });
  } catch (error) {
    return '-';
  }
};

export const formatMarketName = (market: string): string => {
  const marketNames: Record<string, string> = {
    'home_win': 'Victoria Local',
    'draw': 'Empate',
    'away_win': 'Victoria Visitante',
    'over_2_5': 'Más de 2.5 goles',
    'btts_yes': 'Ambos equipos marcan',
  };
  
  return marketNames[market] || market;
};
