import { useEffect, useRef } from 'react';
import { OHLCV } from '@/api/useGetOHLCVs';
import { ColorType, CrosshairMode } from '@/vendor/lightweight-charts/src';
import { LineWidth } from '@/vendor/lightweight-charts/src/renderers/draw-line';
import { UTCTimestamp } from '@/vendor/lightweight-charts/src/model/horz-scale-behavior-time/types';
import { CreatePriceLineOptions } from '@/vendor/lightweight-charts/src/model/price-line-options';
import { createChart } from '@/vendor/lightweight-charts/src/api/create-chart';

// function timeToTz(originalTime: Time, timeZone: string) {
//   const zonedDate = new Date(
//     new Date(Number(originalTime) * 1000).toLocaleString('en-US', { timeZone })
//   );
//   return zonedDate.getTime() / 1000;
// }

export const ChartComponent = (props: {
  data: OHLCV[];
  tp1Price: number | undefined;
  tp2Price: number | undefined;
  tp3Price: number | undefined;
  sl: number | undefined;
  isDarkTheme: boolean;
  setSl: (sl: number) => void;
  setTp1: (sl: number) => void;
  setTp2: (sl: number) => void;
  setTp3: (sl: number) => void;
  setSlToPriceType: () => void;
  setTp1ToPriceType: () => void;
  setTp2ToPriceType: () => void;
  setTp3ToPriceType: () => void;
}) => {
  const {
    data,
    isDarkTheme,
    sl,
    tp1Price,
    tp2Price,
    tp3Price,
    setSl,
    setTp1,
    setTp2,
    setTp3,
    setSlToPriceType,
    setTp1ToPriceType,
    setTp2ToPriceType,
    setTp3ToPriceType,
  } = props;

  const chartContainerRef = useRef();
  useEffect(() => {
    // @ts-ignore
    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: {
          type: ColorType.Solid,
          color: isDarkTheme ? '#222' : 'white',
        },
        textColor: isDarkTheme ? '#D9D9D9' : 'black',
      },
      grid: {
        vertLines: {
          visible: false,
        },
        horzLines: {
          visible: false,
        },
      },
      crosshair: { mode: CrosshairMode.Normal },
      // @ts-ignore
      width: chartContainerRef.current.clientWidth,
      height: 300,
    });

    chart.timeScale().applyOptions({
      rightOffset: 9,
      fixLeftEdge: true,
      timeVisible: true,
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
      lastValueVisible: false,
      priceScaleId: '',
    });
    priceSeries.priceScale().applyOptions({
      scaleMargins: {
        top: 0.01,
        bottom: 0.1, // lowest point will be 40% away from the bottom
      },
    });
    volumeSeries.priceScale().applyOptions({
      scaleMargins: {
        top: 0.9,
        bottom: 0,
      },
    });

    const priceLinesData = [];

    if (tp1Price) {
      const tpLine = {
        price: tp1Price,
        color: '#26a69a',
        lineWidth: 1 as LineWidth,
        lineStyle: 2,
        axisLabelVisible: true,
        title: 'TP1',
        draggable: true,
      };
      priceSeries.createPriceLine(tpLine);
      priceLinesData.push({ value: tp1Price, time: 0 as UTCTimestamp });
    }
    if (tp2Price) {
      const tpLine = {
        price: tp2Price,
        color: '#26a69a',
        lineWidth: 1 as LineWidth,
        lineStyle: 2,
        axisLabelVisible: true,
        title: 'TP2',
        draggable: true,
      };
      priceSeries.createPriceLine(tpLine);
      priceLinesData.push({ value: tp2Price, time: 1 as UTCTimestamp });
    }
    if (tp3Price) {
      const tpLine = {
        price: tp3Price,
        color: '#26a69a',
        lineWidth: 1 as LineWidth,
        lineStyle: 2,
        axisLabelVisible: true,
        title: 'TP3',
        draggable: true,
      };
      priceSeries.createPriceLine(tpLine);
      priceLinesData.push({ value: tp3Price, time: 2 as UTCTimestamp });
    }

    if (sl) {
      const slLine: CreatePriceLineOptions = {
        price: sl,
        color: '#ef5350',
        lineWidth: 1 as LineWidth,
        lineStyle: 2,
        axisLabelVisible: true,
        title: 'SL',
        draggable: true,
      };
      priceSeries.createPriceLine(slLine);
      priceLinesData.push({ value: sl, time: 3 as UTCTimestamp });
    }

    const priceLineSeries = chart.addLineSeries({
      color: 'transparent',
      lastValueVisible: false,
      crosshairMarkerVisible: false,
    });

    priceLineSeries.setData(priceLinesData);

    priceSeries.setData(
      data.map((o) => ({
        open: o.open,
        high: o.high,
        low: o.low,
        close: o.close,
        // time: timeToTz(o.time, Intl.DateTimeFormat().resolvedOptions().timeZone) as UTCTimestamp,
        time: o.time,
      }))
    );
    volumeSeries.setData(
      data.map((element) => ({
        time: element.time,
        value: element.volume,
        color: element.open > element.close ? '#DD5E56' : '#52A49A',
      }))
    );

    chart.subscribeCustomPriceLineDragged((params) => {
      switch (params.customPriceLine.options().title) {
        case 'SL':
          setSlToPriceType();
          setSl(params.customPriceLine.options().price);
          break;
        case 'TP1':
          setTp1ToPriceType();
          setTp1(params.customPriceLine.options().price);
          break;
        case 'TP2':
          setTp2ToPriceType();
          setTp2(params.customPriceLine.options().price);
          break;
        case 'TP3':
          setTp3ToPriceType();
          setTp3(params.customPriceLine.options().price);
          break;
      }
    });

    chart.timeScale().fitContent();
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);

      chart.remove();
    };
  }, [
    data,
    isDarkTheme,
    setSl,
    setSlToPriceType,
    setTp1,
    setTp1ToPriceType,
    setTp2,
    setTp2ToPriceType,
    setTp3,
    setTp3ToPriceType,
    sl,
    tp1Price,
    tp2Price,
    tp3Price,
  ]);

  // @ts-ignore
  return <div ref={chartContainerRef} />;
};
