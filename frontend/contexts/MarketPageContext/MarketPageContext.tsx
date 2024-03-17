import {
  createContext,
  Dispatch,
  ReactNode,
  SetStateAction,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react';
import { useDocumentTitle } from '@mantine/hooks';
import {
  calculateMarketValues,
  MarketCalculatorResponse,
  PriceTypeType,
  Side,
} from '@/app/shared/components/positionCalculators/marketCalculator';
import { useDataLayerContext } from '@/contexts/DataLayerContext/DataLayerContext';
import { GetOHLCVsResponse } from '@/api/useGetOHLCVs';
import { GetTimeframesResponse } from '@/api/useGetTimeframes';
import { GetSymbolsResponse } from '@/api/useGetSymbols';

interface MarketPageContext {
  accountBalance: number | undefined;
  setAccountBalance: Dispatch<SetStateAction<number | undefined>>;
  maxLoss: number | string | undefined;
  selectedAccountId: string | undefined;
  setSelectedAccountId: Dispatch<SetStateAction<string | undefined>>;
  setMaxLoss: Dispatch<SetStateAction<number | string | undefined>>;
  selectedSymbol: string | null;
  setSelectedSymbol: Dispatch<SetStateAction<string | null>>;
  selectedTimeframe: string | null;
  setSelectedTimeframe: Dispatch<SetStateAction<string | null>>;
  sl: number | string | undefined;
  setSl: Dispatch<SetStateAction<number | string | undefined>>;
  maxLossType: PriceTypeType;
  setMaxLossType: Dispatch<SetStateAction<PriceTypeType>>;
  slType: PriceTypeType;
  setSlType: Dispatch<SetStateAction<PriceTypeType>>;
  tp1Type: PriceTypeType;
  setTp1Type: Dispatch<SetStateAction<PriceTypeType>>;
  tp2Type: PriceTypeType;
  setTp2Type: Dispatch<SetStateAction<PriceTypeType>>;
  tp3Type: PriceTypeType;
  setTp3Type: Dispatch<SetStateAction<PriceTypeType>>;
  tp1: number | string | undefined;
  setTp1: Dispatch<SetStateAction<number | string | undefined>>;
  tp2: number | string | undefined;
  setTp2: Dispatch<SetStateAction<number | string | undefined>>;
  tp3: number | string | undefined;
  setTp3: Dispatch<SetStateAction<number | string | undefined>>;
  tp1Percent: number | string | undefined;
  setTp1Percent: Dispatch<SetStateAction<number | string | undefined>>;
  tp2Percent: number | string | undefined;
  setTp2Percent: Dispatch<SetStateAction<number | string | undefined>>;
  tp3Percent: number | string | undefined;
  setTp3Percent: Dispatch<SetStateAction<number | string | undefined>>;
  slToBreakEvenAtTp1: boolean;
  setSlToBreakEvenAtTp1: Dispatch<SetStateAction<boolean>>;
  externalChartHelperURL: string | undefined;
  setExternalChartHelperURL: Dispatch<SetStateAction<string | undefined>>;
  side: Side;
  setSide: Dispatch<SetStateAction<Side>>;
  ohlcvs: GetOHLCVsResponse | undefined;
  timeframes: GetTimeframesResponse | undefined;
  symbols: GetSymbolsResponse | undefined;
  currentPrice: number;
  setCurrentPrice: Dispatch<SetStateAction<number>>;
  fetchSymbolsSuccess: boolean;
  active: number;
  calculatedValues?: MarketCalculatorResponse;
  comment: string;
  setComment: Dispatch<SetStateAction<string>>;
}

export const MarketPageContext = createContext<MarketPageContext>({} as MarketPageContext);

export const useMarketPageContext = () => useContext(MarketPageContext);

export const MarketPageContextProvider = ({ children }: { children: ReactNode }) => {
  const exchange = 'bybit';
  const limit = 1000;
  const dataLayer = useDataLayerContext();
  const [currentPrice, setCurrentPrice] = useState<number>(-1);
  const [accountBalance, setAccountBalance] = useState<number | undefined>(undefined);
  const [selectedAccountId, setSelectedAccountId] = useState<string | undefined>(undefined);
  const [maxLoss, setMaxLoss] = useState<number | string | undefined>(undefined);
  const [selectedSymbol, setSelectedSymbol] = useState<string | null>(null);
  const [selectedTimeframe, setSelectedTimeframe] = useState<string | null>(null);
  const [sl, setSl] = useState<number | string | undefined>(undefined);
  const [maxLossType, setMaxLossType] = useState<PriceTypeType>('%');
  const [slType, setSlType] = useState<PriceTypeType>('%');
  const [tp1Type, setTp1Type] = useState<PriceTypeType>('%');
  const [tp2Type, setTp2Type] = useState<PriceTypeType>('%');
  const [tp3Type, setTp3Type] = useState<PriceTypeType>('%');
  const [tp1, setTp1] = useState<number | string | undefined>(undefined);
  const [tp2, setTp2] = useState<number | string | undefined>(undefined);
  const [tp3, setTp3] = useState<number | string | undefined>(undefined);
  const [tp1Percent, setTp1Percent] = useState<number | string | undefined>(50);
  const [tp2Percent, setTp2Percent] = useState<number | string | undefined>(25);
  const [tp3Percent, setTp3Percent] = useState<number | string | undefined>(25);
  const [slToBreakEvenAtTp1, setSlToBreakEvenAtTp1] = useState(true);
  const [externalChartHelperURL, setExternalChartHelperURL] = useState<string | undefined>(
    undefined
  );
  const [comment, setComment] = useState<string>('');
  const [side, setSide] = useState<Side>('Long');
  const { data: ohlcvs } = dataLayer.useGetOHLCVs({
    exchange,
    symbol: selectedSymbol ?? '',
    timeframe: selectedTimeframe ?? '',
    limit,
  });
  const { data: timeframes } = dataLayer.useGetTimeframes({ exchange });
  const { isSuccess: fetchSymbolsSuccess, data: symbols } = dataLayer.useGetSymbols({ exchange });
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

  const { data } = dataLayer.useGetAccountBalance({ accountId: selectedAccountId });

  useDocumentTitle(
    currentPrice && currentPrice > 0 && selectedSymbol
      ? `${currentPrice} - ${selectedSymbol}`
      : 'Miami Trade'
  );

  useEffect(() => {
    if (!selectedSymbol) {
      // useful after programmatic deslection of symbol
      setCurrentPrice(-1);
    }
  }, [selectedSymbol]);

  useEffect(() => {
    if (data) setAccountBalance(data.balance);
  }, [data]);

  const value = useMemo(
    () => ({
      selectedAccountId,
      setSelectedAccountId,
      accountBalance,
      setAccountBalance,
      maxLoss,
      setMaxLoss,
      selectedSymbol,
      setSelectedSymbol,
      selectedTimeframe,
      setSelectedTimeframe,
      sl,
      setSl,
      maxLossType,
      setMaxLossType,
      slType,
      setSlType,
      tp1Type,
      setTp1Type,
      tp2Type,
      setTp2Type,
      tp3Type,
      setTp3Type,
      tp1,
      setTp1,
      tp2,
      setTp2,
      tp3,
      setTp3,
      tp1Percent,
      setTp1Percent,
      tp2Percent,
      setTp2Percent,
      tp3Percent,
      setTp3Percent,
      slToBreakEvenAtTp1,
      setSlToBreakEvenAtTp1,
      externalChartHelperURL,
      setExternalChartHelperURL,
      side,
      setSide,
      ohlcvs,
      currentPrice,
      setCurrentPrice,
      timeframes,
      calculatedValues,
      fetchSymbolsSuccess,
      symbols,
      active,
      comment,
      setComment,
    }),
    [
      selectedAccountId,
      accountBalance,
      maxLoss,
      selectedSymbol,
      selectedTimeframe,
      sl,
      maxLossType,
      slType,
      tp1Type,
      tp2Type,
      tp3Type,
      tp1,
      tp2,
      tp3,
      tp1Percent,
      tp2Percent,
      tp3Percent,
      slToBreakEvenAtTp1,
      externalChartHelperURL,
      side,
      ohlcvs,
      currentPrice,
      timeframes,
      calculatedValues,
      fetchSymbolsSuccess,
      symbols,
      active,
      comment,
    ]
  );

  return <MarketPageContext.Provider value={value}>{children}</MarketPageContext.Provider>;
};
