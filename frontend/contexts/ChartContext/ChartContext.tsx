import { createContext, useContext } from 'react';
import { IChartApi } from '@/vendor/lightweight-charts/src/api/create-chart';
import { ISeriesApi } from '@/vendor/lightweight-charts/src/api/iseries-api';
import { Time } from '@/vendor/lightweight-charts/src/model/horz-scale-behavior-time/types';
import { IPriceLine } from '@/vendor/lightweight-charts/src/api/iprice-line';

export interface ChartWrapper {
  chart: () => IChartApi;
  _chart: IChartApi | undefined;
  free: () => void;
}

export interface PriceSeriesWrapper {
  series: () => ISeriesApi<'Candlestick', Time>;
  _series: ISeriesApi<'Candlestick', Time> | undefined;
  free: () => void;
}

export interface VolumeSeriesWrapper {
  series: () => ISeriesApi<'Histogram', Time>;
  _series: ISeriesApi<'Histogram', Time> | undefined;
  free: () => void;
}

export interface PriceLineSeriesData {
  series: ISeriesApi<'Line', Time>;
  lines: { tp1: IPriceLine; tp2: IPriceLine; tp3: IPriceLine; sl: IPriceLine };
}

export interface PriceLinesSeriesWrapper {
  data: () => PriceLineSeriesData;
  _data: PriceLineSeriesData | undefined;
  free: () => void;
}

interface ChartContext {
  chartWrapper?: ChartWrapper;
  priceSeriesWrapper?: PriceSeriesWrapper;
  volumeSeriesWrapper?: VolumeSeriesWrapper;
}

export const ChartContext = createContext<ChartContext>({} as ChartContext);

export const useChartContext = () => useContext(ChartContext);
