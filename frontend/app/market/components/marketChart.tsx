import React, { useEffect, useRef, useState } from 'react';
import { useMantineColorScheme } from '@mantine/core';
import socketIOClient, { Socket } from 'socket.io-client';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';
import { ColorType, CrosshairMode, LineStyle } from '@/vendor/lightweight-charts/src';
import { PriceSeries } from '@/app/shared/components/chart/series/priceSeries';
import { PriceLinesSeries } from '@/app/shared/components/chart/series/priceLineSeries';
import { VolumeSeries } from '@/app/shared/components/chart/series/volumeSeries';
import { ChartComponent } from '@/app/shared/components/chart/chartComponent';
import { IChartApi } from '@/vendor/lightweight-charts/src/api/create-chart';
import {
  PriceLinesSeriesWrapper,
  PriceSeriesWrapper,
  VolumeSeriesWrapper,
} from '@/contexts/ChartContext/ChartContext';
import { SeriesDataItemTypeMap } from '@/vendor/lightweight-charts/src/model/data-consumer';
import { UTCTimestamp } from '@/vendor/lightweight-charts/src/model/horz-scale-behavior-time/types';
import { BASE_URL } from '@/app/consts';

const BYBIT_EXCHANGE_NAME = 'bybit';

type OHLCVRealtimeDataType = {
  exchange: string;
  timeframe: string;
  symbol: string;
  ohlcv: number[];
};
export const MarketChart = () => {
  const { colorScheme } = useMantineColorScheme();
  const isDarkTheme = colorScheme === 'dark';
  const {
    setSlType,
    setSl,
    setTp1Type,
    setTp1,
    setTp2Type,
    setTp2,
    setTp3Type,
    setTp3,
    ohlcvs,
    calculatedValues,
    tp1,
    tp2,
    tp3,
    sl,
    selectedSymbol,
    selectedTimeframe,
  } = useMarketPageContext();
  const chartRef = useRef<IChartApi | null>(null);
  const priceSeriesRef = useRef<PriceSeriesWrapper['_series'] | null>(null);
  const volumeSeriesRef = useRef<VolumeSeriesWrapper['_series'] | null>(null);
  const priceLineSeriesRef = useRef<PriceLinesSeriesWrapper['_data'] | null>(null);
  const [currentSocket, setCurrentSocket] = useState<Socket | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_realtimeRoom, setRealtimeRoom] = useState<string>();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_realtimeHandler, setRealtimeHandler] = useState<(data: OHLCVRealtimeDataType) => void>();

  useEffect(() => {
    const priceSeries = priceSeriesRef.current;
    const volumeSeries = volumeSeriesRef.current;

    if (priceSeries === null || volumeSeries === null || !ohlcvs?.ohlcvs) {
      return;
    }

    priceSeries?.setData(
      ohlcvs.ohlcvs.map((o) => ({
        open: o.open,
        high: o.high,
        low: o.low,
        close: o.close,
        // time: timeToTz(o.time, Intl.DateTimeFormat().resolvedOptions().timeZone) as UTCTimestamp,
        time: o.time,
      }))
    );

    volumeSeries?.setData(
      ohlcvs.ohlcvs.map((element) => ({
        time: element.time,
        value: element.volume,
        color: element.open > element.close ? '#DD5E56' : '#52A49A',
      }))
    );
  }, [ohlcvs?.ohlcvs]);

  useEffect(() => {
    const newSocket = socketIOClient(BASE_URL, { transports: ['polling'] });
    newSocket.connect();
    setCurrentSocket(newSocket);
  }, []);

  useEffect(() => {
    const handler = (data: OHLCVRealtimeDataType) => {
      const priceSeries = priceSeriesRef.current;
      const volumeSeries = volumeSeriesRef.current;

      if (
        priceSeries === null ||
        volumeSeries === null ||
        data.exchange !== BYBIT_EXCHANGE_NAME ||
        data.timeframe !== selectedTimeframe ||
        data.symbol !== selectedSymbol
      ) {
        return;
      }

      priceSeries?.update({
        open: data.ohlcv[1],
        high: data.ohlcv[2],
        low: data.ohlcv[3],
        close: data.ohlcv[4],
        time: data.ohlcv[0] as UTCTimestamp,
      });
      volumeSeries?.update({
        value: data.ohlcv[5],
        color: data.ohlcv[1] > data.ohlcv[4] ? '#DD5E56' : '#52A49A',
        time: data.ohlcv[0] as UTCTimestamp,
      });
    };
    currentSocket?.on('ohlcv', handler);
    setRealtimeHandler((prevState: any) => {
      currentSocket?.off('ohlcv', prevState);
      return handler;
    });
  }, [currentSocket, selectedSymbol, selectedTimeframe]);

  useEffect(() => {
    if (!selectedSymbol || !selectedTimeframe) {
      return;
    }
    const room = `${BYBIT_EXCHANGE_NAME}:${selectedSymbol}:${selectedTimeframe}`;

    setRealtimeRoom((prevState) => {
      if (prevState) {
        currentSocket?.emit('leave', room);
      }
      currentSocket?.emit('join', room);
      return room;
    });
  }, [currentSocket, selectedSymbol, selectedTimeframe]);

  useEffect(() => {
    const priceLineSeries = priceLineSeriesRef.current;
    if (priceLineSeries === null || priceLineSeries === undefined) {
      return;
    }

    priceLineSeries.lines.tp1.applyOptions({
      price: calculatedValues.tp1Price,
      lineVisible: tp1 !== undefined,
    });
    priceLineSeries.lines.tp2.applyOptions({
      price: calculatedValues.tp2Price,
      lineVisible: tp2 !== undefined,
    });
    priceLineSeries.lines.tp3.applyOptions({
      price: calculatedValues.tp3Price,
      lineVisible: tp3 !== undefined,
    });
    priceLineSeries.lines.sl.applyOptions({
      price: calculatedValues.slPrice,
      lineVisible: sl !== undefined,
    });

    const priceLinesData: SeriesDataItemTypeMap['Line'][] = [];
    [
      priceLineSeries.lines.sl.options(),
      priceLineSeries.lines.tp1.options(),
      priceLineSeries.lines.tp2.options(),
      priceLineSeries.lines.tp3.options(),
    ].forEach((value, index) => {
      if (value.lineVisible) {
        priceLinesData.push({
          value: value.price,
          time: (Date.now() / 1000 + index) as UTCTimestamp,
        });
      }
    });

    priceLineSeries.series.setData(priceLinesData);
  }, [
    calculatedValues.slPrice,
    calculatedValues.tp1Price,
    calculatedValues.tp2Price,
    calculatedValues.tp3Price,
    sl,
    tp1,
    tp2,
    tp3,
  ]);

  return (
    <ChartComponent
      ref={chartRef}
      options={{
        layout: {
          fontFamily:
            "-apple-system, BlinkMacSystemFont, 'Trebuchet MS', Roboto, Ubuntu, sans-serif",
          fontSize: 12,
          background: {
            type: ColorType.Solid,
            color: isDarkTheme ? '#222' : 'white',
          },
          textColor: isDarkTheme ? '#D9D9D9' : 'black',
        },
        grid: {
          vertLines: {
            color: '#D6DCDE',
            style: LineStyle.Solid,
            visible: false,
          },
          horzLines: {
            color: '#D6DCDE',
            style: LineStyle.Solid,
            visible: false,
          },
        },
        crosshair: {
          horzLine: {
            color: '#758696',
            style: LineStyle.LargeDashed,
            visible: true,
            width: 1,
            labelVisible: true,
            labelBackgroundColor: '#4c525e',
          },
          vertLine: {
            color: '#758696',
            style: LineStyle.LargeDashed,
            visible: true,
            width: 1,
            labelVisible: true,
            labelBackgroundColor: '#4c525e',
          },
          mode: CrosshairMode.Normal,
        },
      }}
      updateSlAfterDragging={(newSL) => {
        setSlType('$');
        setSl(newSL);
      }}
      updateTP1AfterDragging={(newTP) => {
        setTp1Type('$');
        setTp1(newTP);
      }}
      updateTP2AfterDragging={(newTP) => {
        setTp2Type('$');
        setTp2(newTP);
      }}
      updateTP3AfterDragging={(newTP) => {
        setTp3Type('$');
        setTp3(newTP);
      }}
    >
      <PriceSeries ref={priceSeriesRef}>
        <PriceLinesSeries ref={priceLineSeriesRef} />
      </PriceSeries>
      <VolumeSeries ref={volumeSeriesRef} />
    </ChartComponent>
  );
};
