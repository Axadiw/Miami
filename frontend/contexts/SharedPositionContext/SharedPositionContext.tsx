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
import { PriceTypeType, Side } from '@/app/market/components/positionCalculators/marketCalculator';
import { useDataLayerContext } from '@/contexts/DataLayerContext/DataLayerContext';
import { GetOHLCVsResponse } from '@/api/useGetOHLCVs';
import { GetTimeframesResponse } from '@/api/useGetTimeframes';
import { GetSymbolsResponse } from '@/api/useGetSymbols';

interface SharedPositionContext {
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
  comment: string;
  setComment: Dispatch<SetStateAction<string>>;
  softStopLossTimeout: number | string | undefined;
  setSoftStopLossTimeout: Dispatch<SetStateAction<number | string | undefined>>;
  softStopLossEnabled: boolean;
  setSoftStopLossEnabled: Dispatch<SetStateAction<boolean>>;
  chartAutoSize: boolean;
  setChartAutoSize: Dispatch<SetStateAction<boolean>>;
}

export const SharedPositionContext = createContext<SharedPositionContext>(
  {} as SharedPositionContext
);

export const useSharedPositionContext = () => useContext(SharedPositionContext);

export const SharedPositionContextProvider = ({ children }: { children: ReactNode }) => {
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
  const [chartAutoSize, setChartAutoSize] = useState(true);
  const [externalChartHelperURL, setExternalChartHelperURL] = useState<string | undefined>(
    undefined
  );
  const [softStopLossTimeout, setSoftStopLossTimeout] = useState<number | string | undefined>(
    undefined
  );
  const [softStopLossEnabled, setSoftStopLossEnabled] = useState(false);
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

  const { data } = dataLayer.useGetAccountBalance({ accountId: selectedAccountId });

  useDocumentTitle(
    currentPrice && currentPrice > 0 && selectedSymbol
      ? `${currentPrice} - ${selectedSymbol}`
      : 'Miami Trade'
  );

  useEffect(() => {
    if (!selectedSymbol) {
      // useful after programmatic deselection of symbol
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
      fetchSymbolsSuccess,
      symbols,
      comment,
      setComment,
      softStopLossTimeout,
      setSoftStopLossTimeout,
      softStopLossEnabled,
      setSoftStopLossEnabled,
      chartAutoSize,
      setChartAutoSize,
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
      fetchSymbolsSuccess,
      symbols,
      comment,
      softStopLossTimeout,
      softStopLossEnabled,
      chartAutoSize,
    ]
  );

  return <SharedPositionContext.Provider value={value}>{children}</SharedPositionContext.Provider>;
};
