import { useLimitPositionContext } from '@/app/limit/contexts/LimitPositionContext/LimitPositionContext';
import { useSharedPositionContext } from '@/contexts/SharedPositionContext/SharedPositionContext';

export const useLimitPositionDetailsValidators = () => {
  const { limitPrice } = useLimitPositionContext();
  const { side, currentPrice } = useSharedPositionContext();

  return {
    limitPriceAbove0:
      limitPrice !== undefined && Number(limitPrice) <= 0
        ? 'Limit price need to be above 0'
        : undefined,
    limitPriceAboveCurrentPriceWhenShort:
      side === 'Short' && limitPrice !== undefined && Number(limitPrice) < currentPrice
        ? 'Limit Price need to be above current price when shorting'
        : undefined,
    limitPriceBelowCurrentPriceWhenLong:
      side === 'Long' && limitPrice !== undefined && Number(limitPrice) > currentPrice
        ? 'Limit Price need to be below current price when longing'
        : undefined,
  };
};
