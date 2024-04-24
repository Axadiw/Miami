import {
  createContext,
  Dispatch,
  ReactNode,
  SetStateAction,
  useContext,
  useMemo,
  useState,
} from 'react';
import { useSharedPositionContext } from '@/contexts/SharedPositionContext/SharedPositionContext';
import {
  calculateMarketValues,
  MarketCalculatorResponse,
} from '@/app/shared/components/positionCalculators/marketCalculator';

interface LimitPositionContext {
  setLimitPrice: Dispatch<SetStateAction<number | string | undefined>>;
  limitPrice: number | string | undefined;
  calculatedValues?: MarketCalculatorResponse;
  active: number;
}

export const LimitPositionContext = createContext<LimitPositionContext>({} as LimitPositionContext);

export const useLimitPositionContext = () => useContext(LimitPositionContext);

export const LimitPositionContextProvider = ({ children }: { children: ReactNode }) => {
  const [limitPrice, setLimitPrice] = useState<number | string | undefined>(undefined);
  const {
    sl,
    tp1,
    tp2,
    tp3,
    side,
    tp1Percent,
    tp2Percent,
    tp3Percent,
    accountBalance,
    maxLoss,
    maxLossType,
    slType,
    tp1Type,
    tp2Type,
    tp3Type,
    selectedSymbol,
    selectedAccountId,
  } = useSharedPositionContext();

  const calculatedValues =
    accountBalance && limitPrice
      ? calculateMarketValues({
          side,
          openPrice: Number(limitPrice),
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

  // TODO: share logic with other contexts
  const step0Finished = selectedAccountId !== undefined;
  const step1Finished = selectedSymbol !== null;
  const step2Finished = limitPrice !== undefined && maxLoss !== undefined && sl !== undefined;
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
      limitPrice,
      setLimitPrice,
      calculatedValues,
      active,
    }),
    [active, calculatedValues, limitPrice]
  );

  return <LimitPositionContext.Provider value={value}>{children}</LimitPositionContext.Provider>;
};
