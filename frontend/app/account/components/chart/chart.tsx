import {
  CandlestickData,
  ColorType,
  createChart,
  CrosshairMode,
  LineWidth,
} from 'lightweight-charts';
import { useEffect, useRef } from 'react';
import { OHLCV } from '@/api/useGetOHLCVs';

export const ChartComponent = (props: {
  data: OHLCV[];
  tp1Price: number | undefined;
  tp2Price: number | undefined;
  tp3Price: number | undefined;
  sl: number | undefined;
  isDarkTheme: boolean;
}) => {
  const { data, isDarkTheme, sl, tp1Price, tp2Price, tp3Price } = props;

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

    if (sl) {
      const slLine = {
        price: sl,
        color: '#ef5350',
        lineWidth: 1 as LineWidth,
        lineStyle: 2, // LineStyle.Dashed
        axisLabelVisible: true,
        title: 'SL',
      };
      priceSeries.createPriceLine(slLine);
    }

    if (tp1Price) {
      const tpLine = {
        price: tp1Price,
        color: '#26a69a',
        lineWidth: 1 as LineWidth,
        lineStyle: 2,
        axisLabelVisible: true,
        title: 'TP1',
      };
      priceSeries.createPriceLine(tpLine);
    }
    if (tp2Price) {
      const tpLine = {
        price: tp2Price,
        color: '#26a69a',
        lineWidth: 1 as LineWidth,
        lineStyle: 2,
        axisLabelVisible: true,
        title: 'TP2',
      };
      priceSeries.createPriceLine(tpLine);
    }
    if (tp3Price) {
      const tpLine = {
        price: tp3Price,
        color: '#26a69a',
        lineWidth: 1 as LineWidth,
        lineStyle: 2,
        axisLabelVisible: true,
        title: 'TP3',
      };
      priceSeries.createPriceLine(tpLine);
    }

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);

      chart.remove();
    };
  }, [data, isDarkTheme, sl, tp1Price, tp2Price, tp3Price]);

  // @ts-ignore
  return <div ref={chartContainerRef} />;
};
