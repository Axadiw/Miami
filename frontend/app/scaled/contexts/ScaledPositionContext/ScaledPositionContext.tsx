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
import { MarketCalculatorResponse } from '@/app/market/components/positionCalculators/marketCalculator';
import { calculateScaledValues } from '@/app/scaled/components/positionCalculators/scaledCalculator';

interface ScaledPositionContext {
  setUpperPrice: Dispatch<SetStateAction<number | string | undefined>>;
  upperPrice: number | string | undefined;
  setLowerPrice: Dispatch<SetStateAction<number | string | undefined>>;
  lowerPrice: number | string | undefined;
  setOrdersCount: Dispatch<SetStateAction<number | string | undefined>>;
  ordersCount: number | string | undefined;
  calculatedValues?: MarketCalculatorResponse;
  active: number;
}

export const ScaledPositionContext = createContext<ScaledPositionContext>(
  {} as ScaledPositionContext
);

export const useScaledPositionContext = () => useContext(ScaledPositionContext);

export const ScaledPositionContextProvider = ({ children }: { children: ReactNode }) => {
  const [upperPrice, setUpperPrice] = useState<number | string | undefined>(undefined);
  const [lowerPrice, setLowerPrice] = useState<number | string | undefined>(undefined);
  const [ordersCount, setOrdersCount] = useState<number | string | undefined>(undefined);
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
    accountBalance && upperPrice
      ? calculateScaledValues({
          side,
          upperPrice: Number(upperPrice),
          lowerPrice: Number(lowerPrice),
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
  const step2Finished =
    upperPrice !== undefined &&
    lowerPrice !== undefined &&
    ordersCount !== undefined &&
    maxLoss !== undefined &&
    sl !== undefined;
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
      upperPrice,
      setUpperPrice,
      lowerPrice,
      setLowerPrice,
      calculatedValues,
      active,
      ordersCount,
      setOrdersCount,
    }),
    [active, calculatedValues, lowerPrice, ordersCount, upperPrice]
  );

  return <ScaledPositionContext.Provider value={value}>{children}</ScaledPositionContext.Provider>;
};
