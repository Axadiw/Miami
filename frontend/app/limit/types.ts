import { ISeriesApi } from '@/vendor/lightweight-charts/src/api/iseries-api';
import { Time } from '@/vendor/lightweight-charts/src/model/horz-scale-behavior-time/types';
import { IPriceLine } from '@/vendor/lightweight-charts/src/api/iprice-line';

export interface LimitPriceLineSeriesData {
  series: ISeriesApi<'Line', Time>;
  lines: { limit: IPriceLine; tp1: IPriceLine; tp2: IPriceLine; tp3: IPriceLine; sl: IPriceLine };
}

export interface LimitPriceLinesSeriesWrapper {
  data: () => LimitPriceLineSeriesData;
  _data: LimitPriceLineSeriesData | undefined;
  free: () => void;
}
