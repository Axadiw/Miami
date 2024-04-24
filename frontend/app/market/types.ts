import { ISeriesApi } from '@/vendor/lightweight-charts/src/api/iseries-api';
import { Time } from '@/vendor/lightweight-charts/src/model/horz-scale-behavior-time/types';
import { IPriceLine } from '@/vendor/lightweight-charts/src/api/iprice-line';

export interface MarketPriceLineSeriesData {
  series: ISeriesApi<'Line', Time>;
  lines: { tp1: IPriceLine; tp2: IPriceLine; tp3: IPriceLine; sl: IPriceLine };
}

export interface MarketPriceLinesSeriesWrapper {
  data: () => MarketPriceLineSeriesData;
  _data: MarketPriceLineSeriesData | undefined;
  free: () => void;
}
