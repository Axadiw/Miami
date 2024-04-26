import { useSharedPositionContext } from '@/contexts/SharedPositionContext/SharedPositionContext';
import { useScaledPositionContext } from '@/app/scaled/contexts/ScaledPositionContext/ScaledPositionContext';

export const useScaledPositionDetailsValidators = () => {
  const { upperPrice, lowerPrice, ordersCount, upperPriceAsCurrent } = useScaledPositionContext();
  const { side, currentPrice } = useSharedPositionContext();

  return {
    UpperAboveLower:
      upperPrice !== undefined &&
      lowerPrice !== undefined &&
      Number(upperPrice) <= Number(lowerPrice)
        ? 'Upper price need to above lower price'
        : undefined,
    OrdersCountIsInteger:
      ordersCount !== undefined && Number(ordersCount) % 1 !== 0
        ? 'Orders count should be integer'
        : undefined,
    UpperPriceAbove0:
      upperPrice !== undefined && Number(upperPrice) <= 0
        ? 'Upper price need to be above 0'
        : undefined,
    LowerPriceAbove0:
      lowerPrice !== undefined && Number(lowerPrice) <= 0
        ? 'Lower price need to be above 0'
        : undefined,
    OrdersCountAbove2:
      ordersCount !== undefined && Number(ordersCount) <= 2
        ? 'Orders count need to be above 2'
        : undefined,
    RangeAboveCurrentPriceWhenShort:
      side === 'Short' &&
      lowerPrice !== undefined &&
      Number(lowerPrice) < currentPrice &&
      upperPriceAsCurrent !== false
        ? 'Orders need to be above current price when shorting'
        : undefined,
    RangeBelowCurrentPriceWhenLong:
      side === 'Long' &&
      upperPrice !== undefined &&
      Number(upperPrice) > currentPrice &&
      upperPriceAsCurrent !== true
        ? 'Orders need to be below current price when longing'
        : undefined,
  };
};
