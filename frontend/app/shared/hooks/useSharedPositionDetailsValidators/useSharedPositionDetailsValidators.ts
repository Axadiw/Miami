import { useSharedPositionContext } from '@/contexts/SharedPositionContext/SharedPositionContext';
import { MarketCalculatorResponse } from '@/app/market/components/positionCalculators/marketCalculator';

export const useSharedPositionDetailsValidators = (calculatedValues?: MarketCalculatorResponse) => {
  const {
    side,
    tp1Percent,
    tp2Percent,
    tp3Percent,
    comment,
    sl,
    tp1,
    tp2,
    tp3,
    maxLoss,
    softStopLossTimeout,
    softStopLossEnabled,
  } = useSharedPositionContext();

  return {
    slBelowOpen:
      sl && calculatedValues && calculatedValues.slPercent < 0
        ? `SL should be ${side === 'Long' ? 'below' : 'above'} current price`
        : undefined,
    tp1AboveOpen:
      tp1 && calculatedValues && calculatedValues.tp1Percent < 0
        ? `TP1 should be ${side === 'Long' ? 'above' : 'below'} current price`
        : undefined,
    tp2AboveTp1:
      tp2 && tp1 && calculatedValues && calculatedValues.tp1Percent >= calculatedValues.tp2Percent
        ? `TP2 should be ${side === 'Long' ? 'above' : 'below'} TP1`
        : undefined,
    tp3AboveTp2:
      tp3 && tp2 && calculatedValues && calculatedValues.tp2Percent >= calculatedValues.tp3Percent
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
      maxLoss && calculatedValues && calculatedValues.maxLossUSD <= 0
        ? 'You need to specify maximum loss'
        : undefined,
    slAbove0:
      sl && calculatedValues && calculatedValues.slPercent <= 0
        ? 'SL need to be above 0%'
        : undefined,
    tp1Above0:
      tp1 && calculatedValues && calculatedValues.tp1Percent <= 0
        ? 'TP1 need to be above 0%'
        : undefined,
    tp2Above0:
      tp2 && calculatedValues && calculatedValues.tp2Percent <= 0
        ? 'TP2 need to be above 0%'
        : undefined,
    tp3Above0:
      tp3 && calculatedValues && calculatedValues.tp3Percent <= 0
        ? 'TP3 need to be above 0%'
        : undefined,
    commentNotTooLong: comment && comment.length > 1000 ? 'Comment too long' : undefined,
    softSlAbove0:
      softStopLossEnabled && softStopLossTimeout && +softStopLossTimeout <= 0
        ? 'Soft stop loss needs to be above 0'
        : undefined,
    softSlNotUndefined:
      softStopLossEnabled && !softStopLossTimeout ? "Soft stop loss can't be empty" : undefined,
  };
};
