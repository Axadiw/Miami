import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';

export const usePositionDetailsValidators = () => {
  const { calculatedValues, side, tp1Percent, tp2Percent, tp3Percent } = useMarketPageContext();

  return {
    slBelowOpen:
      calculatedValues.slPercent < 0
        ? `SL should be ${side === 'Long' ? 'below' : 'above'} current price`
        : undefined,
    tp1AboveOpen:
      calculatedValues.tp1Percent < 0
        ? `TP1 should be ${side === 'Long' ? 'above' : 'below'} current price`
        : undefined,
    tp2AboveTp1:
      calculatedValues.tp1Percent >= calculatedValues.tp2Percent
        ? `TP2 should be ${side === 'Long' ? 'above' : 'below'} TP1`
        : undefined,
    tp3AboveTp2:
      calculatedValues.tp2Percent >= calculatedValues.tp3Percent
        ? `TP3 should be ${side === 'Long' ? 'above' : 'below'} TP2`
        : undefined,
    tpVolumesAddTo100:
      tp1Percent &&
      tp2Percent &&
      tp3Percent &&
      Number(tp1Percent) + Number(tp2Percent) + Number(tp3Percent) !== 100
        ? 'Take profit volumes should add up to 100%'
        : undefined,
    maximumLossAbove0:
      calculatedValues.maxLossUSD <= 0 ? 'You need to specify maximum loss' : undefined,
    slAbove0: calculatedValues.slPercent <= 0 ? 'SL need to be above 0%' : undefined,
    tp1Above0: calculatedValues.tp1Percent <= 0 ? 'TP1 need to be above 0%' : undefined,
    tp2Above0: calculatedValues.tp2Percent <= 0 ? 'TP2 need to be above 0%' : undefined,
    tp3Above0: calculatedValues.tp3Percent <= 0 ? 'TP3 need to be above 0%' : undefined,
  };
};
