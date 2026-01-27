import {
  formatOdds,
  formatPercentage,
  formatEV,
  formatStake,
  getConfidenceColor,
  formatMarketName,
} from '../utils/formatters';

describe('Formatters', () => {
  describe('formatOdds', () => {
    it('should format odds correctly', () => {
      expect(formatOdds(2.5)).toBe('2.50');
      expect(formatOdds(3.123)).toBe('3.12');
    });

    it('should handle invalid values', () => {
      expect(formatOdds(NaN)).toBe('-');
      expect(formatOdds(null as any)).toBe('-');
    });
  });

  describe('formatPercentage', () => {
    it('should format percentage correctly', () => {
      expect(formatPercentage(45.678)).toBe('45.7%');
      expect(formatPercentage(10)).toBe('10.0%');
    });

    it('should handle invalid values', () => {
      expect(formatPercentage(NaN)).toBe('-');
    });
  });

  describe('formatEV', () => {
    it('should format positive EV with + sign', () => {
      const result = formatEV(5.5);
      expect(result.text).toBe('+5.5%');
      expect(result.color).toBe('#27ae60');
    });

    it('should format negative EV with - sign', () => {
      const result = formatEV(-2.3);
      expect(result.text).toBe('-2.3%');
      expect(result.color).toBe('#e74c3c');
    });
  });

  describe('formatStake', () => {
    it('should format stake with euro symbol', () => {
      expect(formatStake(100)).toBe('100.00€');
      expect(formatStake(25.5)).toBe('25.50€');
    });
  });

  describe('getConfidenceColor', () => {
    it('should return correct color based on EV', () => {
      expect(getConfidenceColor(6)).toBe('#27ae60'); // Green
      expect(getConfidenceColor(4)).toBe('#3498db'); // Blue
      expect(getConfidenceColor(1)).toBe('#95a5a6'); // Gray
      expect(getConfidenceColor(-2)).toBe('#e74c3c'); // Red
    });
  });

  describe('formatMarketName', () => {
    it('should translate market names', () => {
      expect(formatMarketName('home_win')).toBe('Victoria Local');
      expect(formatMarketName('draw')).toBe('Empate');
      expect(formatMarketName('away_win')).toBe('Victoria Visitante');
      expect(formatMarketName('over_2_5')).toBe('Más de 2.5 goles');
      expect(formatMarketName('btts_yes')).toBe('Ambos equipos marcan');
    });

    it('should return original for unknown markets', () => {
      expect(formatMarketName('unknown_market')).toBe('unknown_market');
    });
  });
});
