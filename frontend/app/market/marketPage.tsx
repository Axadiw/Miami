'use client';

import { Button, Select, useMantineColorScheme } from '@mantine/core';
import { useEffect, useRef, useState } from 'react';
import {
  CandlestickData,
  ChartOptions,
  ColorType,
  createChart,
  CrosshairMode,
  DeepPartial,
} from 'lightweight-charts';
import { useDataLayerContext } from '@/contexts/DataLayerContext/DataLayerContext';
import { OHLCV } from '@/api/useGetOHLCVs';

const ChartComponent = (props: { data: OHLCV[]; options: DeepPartial<ChartOptions> }) => {
  const { data, options } = props;

  const chartContainerRef = useRef();
  useEffect(() => {
    // @ts-ignore
    const chart = createChart(chartContainerRef.current, {
      ...options,
      crosshair: { mode: CrosshairMode.Normal },
      // @ts-ignore
      width: chartContainerRef.current.clientWidth,
      height: 300,
    });
    const handleResize = () => {
      // @ts-ignore
      chart.applyOptions({ width: chartContainerRef.current.clientWidth });
    };

    const priceSeries = chart.addCandlestickSeries({
      priceFormat: { precision: 6, minMove: 0.000001 },
    });
    const volumeSeries = chart.addHistogramSeries({
      priceFormat: {
        type: 'volume',
      },
      priceScaleId: '',
    });
    volumeSeries.priceScale().applyOptions({
      scaleMargins: {
        top: 0.7,
        bottom: 0,
      },
    });

    priceSeries.setData(data as CandlestickData[]);
    volumeSeries.setData(
      data.map((element) => ({
        time: element.time,
        value: element.volume,
        color: element.open > element.close ? '#DD5E56' : '#52A49A',
      }))
    );

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);

      chart.remove();
    };
  }, [data, options]);

  // @ts-ignore
  return <div ref={chartContainerRef} />;
};

export default function MarketPage() {
  const exchange = 'bybit';
  const limit = 1000;
  const [selectedSymbol, setSelectedSymbol] = useState<string | null>(null);
  const [selectedTimeframe, setSelectedTimeframe] = useState<string | null>(null);

  const { colorScheme } = useMantineColorScheme();
  const isDarkTheme = colorScheme === 'dark';
  const dataLayer = useDataLayerContext();
  const { data: timeframes } = dataLayer.useGetTimeframes({ exchange });

  const { data: ohlcvs } = dataLayer.useGetOHLCVs({
    exchange,
    symbol: selectedSymbol ?? '',
    timeframe: selectedTimeframe ?? '',
    limit,
  });

  useEffect(() => {
    if (timeframes && timeframes.timeframes.length > 0) {
      setSelectedTimeframe(timeframes.timeframes.includes('1h') ? '1h' : timeframes.timeframes[0]);
    }
  }, [timeframes]);

  const { isSuccess: fetchSymbolsSuccess, data: symbols } = dataLayer.useGetSymbols({ exchange });
  return (
    <>
      {fetchSymbolsSuccess && (
        <Select
          label="Symbol"
          placeholder="Pick symbol"
          data={symbols.symbols}
          value={selectedSymbol}
          onChange={setSelectedSymbol}
          searchable
        />
      )}
      {ohlcvs && (
        <ChartComponent
          options={{
            layout: {
              background: {
                type: ColorType.Solid,
                color: isDarkTheme ? '#222' : 'white',
              },
              textColor: isDarkTheme ? '#D9D9D9' : 'black',
            },
            grid: {
              vertLines: {
                color: isDarkTheme ? '#2B2B43' : '#E4FFE9',
              },
            },
          }}
          data={ohlcvs.ohlcvs}
        />
      )}
      {timeframes &&
        timeframes.timeframes.map((timeframe) => (
          <Button
            key={`tf-${timeframe}`}
            variant={timeframe === selectedTimeframe ? 'filled' : 'default'}
            size="xs"
            onClick={() => setSelectedTimeframe(timeframe)}
          >
            {timeframe}
          </Button>
        ))}
    </>
  );
}
