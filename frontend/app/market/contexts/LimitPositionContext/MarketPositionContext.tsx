import { createContext, ReactNode, useContext, useMemo } from 'react';
import {
  calculateMarketValues,
  MarketCalculatorResponse,
} from '@/app/shared/components/positionCalculators/marketCalculator';
import { useSharedPositionContext } from '@/contexts/SharedPositionContext/SharedPositionContext';

interface MarketPositionContext {
  calculatedValues?: MarketCalculatorResponse;
  active: number;
}

export const MarketPositionContext = createContext<MarketPositionContext>(
  {} as MarketPositionContext
);

export const useMarketPositionContext = () => useContext(MarketPositionContext);

export const MarketPositionContextProvider = ({ children }: { children: ReactNode }) => {
  const {
    sl,
    tp1,
    tp2,
    tp3,
    side,
    tp1Percent,
    tp2Percent,
    tp3Percent,
    currentPrice,
    accountBalance,
    maxLoss,
    maxLossType,
    slType,
    tp1Type,
    tp2Type,
    tp3Type,
    selectedAccountId,
    selectedSymbol,
  } = useSharedPositionContext();

  const calculatedValues = accountBalance
    ? calculateMarketValues({
        side,
        openPrice: currentPrice,
        accountBalance,
        maxLoss,
        maxLossType,
        sl,
        tp1,
        tp2,
        tp3,
        tp1Percent,
        tp2Percent,
        tp3Percent,
        slType,
        tp1Type,
        tp2Type,
        tp3Type,
      })
    : undefined;

  const step0Finished = selectedAccountId !== undefined;
  const step1Finished = selectedSymbol !== null;
  const step2Finished = maxLoss !== undefined && sl !== undefined;
  const step3Finished =
    tp1 !== undefined &&
    tp1Percent !== undefined &&
    tp2 !== undefined &&
    tp2Percent !== undefined &&
    tp3 !== undefined &&
    tp3Percent !== undefined;

  let active = 0;
  if (step0Finished) {
    active = 1;
  }
  if (step1Finished) {
    active = 2;
  }
  if (step1Finished && step2Finished) {
    active = 3;
  }
  if (step1Finished && step2Finished && step3Finished) {
    active = 4;
  }

  const value = useMemo(
    () => ({
      calculatedValues,
      active,
    }),
    [active, calculatedValues]
  );

  return <MarketPositionContext.Provider value={value}>{children}</MarketPositionContext.Provider>;
};
