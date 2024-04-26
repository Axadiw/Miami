import React, { useEffect, useRef, useState } from 'react';
import { useMantineColorScheme } from '@mantine/core';
import socketIOClient, { Socket } from 'socket.io-client';
import { ColorType, CrosshairMode, LineStyle } from '@/vendor/lightweight-charts/src';
import { IChartApi } from '@/vendor/lightweight-charts/src/api/create-chart';
import { PriceSeriesWrapper, VolumeSeriesWrapper } from '@/contexts/ChartContext/ChartContext';
import { SeriesDataItemTypeMap } from '@/vendor/lightweight-charts/src/model/data-consumer';
import { UTCTimestamp } from '@/vendor/lightweight-charts/src/model/horz-scale-behavior-time/types';
import { BASE_URL } from '@/app/consts';
import { useSharedPositionContext } from '@/contexts/SharedPositionContext/SharedPositionContext';
import { MarketCalculatorResponse } from '@/app/market/components/positionCalculators/marketCalculator';
import { PriceSeries } from '@/app/shared/components/chart/priceSeries';
import { VolumeSeries } from '@/app/shared/components/chart/volumeSeries';
import { useScaledPositionContext } from '@/app/scaled/contexts/ScaledPositionContext/ScaledPositionContext';
import { ScaledPriceLinesSeriesWrapper } from '@/app/scaled/types';
import { ScaledChartComponent } from '@/app/scaled/components/chart/scaledChartComponent';
import { ScaledPriceLinesSeries } from '@/app/scaled/components/chart/series/scaledPriceLineSeries';

const BYBIT_EXCHANGE_NAME = 'bybit';

type OHLCVRealtimeDataType = {
  exchange: string;
  timeframe: string;
  symbol: string;
  ohlcv: number[];
};

function timeToLocal(originalTime: number) {
  const d = new Date(originalTime * 1000);
  return (
    Date.UTC(
      d.getFullYear(),
      d.getMonth(),
      d.getDate(),
      d.getHours(),
      d.getMinutes(),
      d.getSeconds(),
      d.getMilliseconds()
    ) / 1000
  );
}

export interface ScaledChartProps {
  calculatedValues?: MarketCalculatorResponse;
}

export const ScaledChart = (props: ScaledChartProps) => {
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
    tp1,
    tp2,
    tp3,
    sl,
    selectedSymbol,
    selectedTimeframe,
    setCurrentPrice,
    chartAutoSize,
  } = useSharedPositionContext();

  const {
    upperPrice,
    setUpperPrice,
    lowerPrice,
    setLowerPrice,
    upperPriceAsCurrent,
    setUpperPriceAsCurrent,
  } = useScaledPositionContext();

  const { calculatedValues } = props;

  const chartRef = useRef<IChartApi | null>(null);
  const priceSeriesRef = useRef<PriceSeriesWrapper['_series'] | null>(null);
  const volumeSeriesRef = useRef<VolumeSeriesWrapper['_series'] | null>(null);
  const priceLineSeriesRef = useRef<ScaledPriceLinesSeriesWrapper['_data'] | null>(null);
  const [currentSocket, setCurrentSocket] = useState<Socket | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_realtimeRoom, setRealtimeRoom] = useState<string>();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_realtimeHandler, setRealtimeHandler] = useState<(data: OHLCVRealtimeDataType) => void>();

  useEffect(() => {
    const priceSeries = priceSeriesRef.current;
    const volumeSeries = volumeSeriesRef.current;

    if (!priceSeries || !volumeSeries || !ohlcvs?.ohlcvs) {
      return;
    }

    if (!selectedSymbol) {
      // useful when programmatically deselecting symbol
      chartRef?.current?.remove();
    }

    priceSeries?.setData(
      ohlcvs.ohlcvs.map((o) => ({
        open: o.open,
        high: o.high,
        low: o.low,
        close: o.close,
        time: timeToLocal(+o.time) as UTCTimestamp,
      }))
    );
    const lastPrice = ohlcvs?.ohlcvs.at(-1)?.close;
    if (lastPrice) {
      setCurrentPrice(lastPrice);
    }

    volumeSeries?.setData(
      ohlcvs.ohlcvs.map((element) => ({
        time: timeToLocal(+element.time) as UTCTimestamp,
        value: element.volume,
        color: element.open > element.close ? '#DD5E56' : '#52A49A',
      }))
    );
  }, [ohlcvs?.ohlcvs, selectedSymbol, setCurrentPrice]);

  useEffect(() => {
    priceSeriesRef?.current?.priceScale().applyOptions({
      autoScale: chartAutoSize,
    });
    priceLineSeriesRef?.current?.series.priceScale().applyOptions({ autoScale: chartAutoSize });
  }, [chartAutoSize]);

  useEffect(() => {
    const newSocket = socketIOClient(BASE_URL);
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
        time: timeToLocal(data.ohlcv[0]) as UTCTimestamp,
      });
      setCurrentPrice(data.ohlcv[4]);
      volumeSeries?.update({
        value: data.ohlcv[5],
        color: data.ohlcv[1] > data.ohlcv[4] ? '#DD5E56' : '#52A49A',
        time: timeToLocal(data.ohlcv[0]) as UTCTimestamp,
      });
    };
    currentSocket?.on('ohlcv', handler);
    setRealtimeHandler((prevState: any) => {
      currentSocket?.off('ohlcv', prevState);
      return handler;
    });
  }, [currentSocket, selectedSymbol, selectedTimeframe, setCurrentPrice]);

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
    if (
      priceLineSeries === null ||
      priceLineSeries === undefined ||
      calculatedValues === undefined
    ) {
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
    priceLineSeries.lines.upper.applyOptions({
      price: Number(upperPrice),
      lineVisible: upperPrice !== undefined,
    });
    priceLineSeries.lines.lower.applyOptions({
      price: Number(lowerPrice),
      lineVisible: lowerPrice !== undefined,
    });
    const priceLinesData: SeriesDataItemTypeMap['Line'][] = [];
    [
      priceLineSeries.lines.sl.options(),
      priceLineSeries.lines.tp1.options(),
      priceLineSeries.lines.tp2.options(),
      priceLineSeries.lines.tp3.options(),
      priceLineSeries.lines.upper.options(),
      priceLineSeries.lines.lower.options(),
    ].forEach((value, index) => {
      if (value.lineVisible) {
        priceLinesData.push({
          value: value.price,
          time: (Math.floor(Date.now() / 1000 / 60) + index * 60) as UTCTimestamp,
        });
      }
    });

    priceLineSeries.series.setData(priceLinesData);
  }, [calculatedValues, upperPrice, sl, tp1, tp2, tp3, lowerPrice]);

  return (
    <ScaledChartComponent
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
      updateUpperAfterDragging={(newUpper) => {
        setUpperPrice(newUpper);
        if (upperPriceAsCurrent === true) {
          setUpperPriceAsCurrent(undefined);
        }
      }}
      updateLowerAfterDragging={(newLower) => {
        setLowerPrice(newLower);
        if (upperPriceAsCurrent === false) {
          setUpperPriceAsCurrent(undefined);
        }
      }}
    >
      <PriceSeries ref={priceSeriesRef}>
        <ScaledPriceLinesSeries ref={priceLineSeriesRef} />
      </PriceSeries>
      <VolumeSeries ref={volumeSeriesRef} />
    </ScaledChartComponent>
  );
};
