/* eslint-disable react/no-this-in-sfc */
import { forwardRef, useImperativeHandle, useLayoutEffect, useRef } from 'react';
import { useChartContext } from '@/contexts/ChartContext/ChartContext';
import { LineWidth } from '@/vendor/lightweight-charts/src/renderers/draw-line';
import { MarketPriceLinesSeriesWrapper } from '@/app/market/types';

interface MarketPriceLineSeriesProps {}

export const MarketPriceLinesSeries = forwardRef((props: MarketPriceLineSeriesProps, ref) => {
  const { chartWrapper, priceSeriesWrapper } = useChartContext();

  const context = useRef({
    data() {
      if (!this._data && priceSeriesWrapper && chartWrapper?.chart()) {
        const commonOptions = {
          price: 0,
          lineWidth: 1 as LineWidth,
          lineStyle: 2,
          axisLabelVisible: true,
          color: '#26a69a',
          draggable: true,
          lineVisible: false,
        };
        const lines = {
          tp1: priceSeriesWrapper?.series().createPriceLine({ ...commonOptions, title: 'TP1' }),
          tp2: priceSeriesWrapper?.series().createPriceLine({ ...commonOptions, title: 'TP2' }),
          tp3: priceSeriesWrapper?.series().createPriceLine({ ...commonOptions, title: 'TP3' }),
          sl: priceSeriesWrapper
            ?.series()
            .createPriceLine({ ...commonOptions, title: 'SL', color: '#ef5350' }),
        };

        const series = chartWrapper?.chart().addLineSeries({
          color: 'transparent',
          lastValueVisible: false,
          crosshairMarkerVisible: false,
        });

        this._data = {
          lines,
          series,
        };
      }
      return this._data;
    },
    free() {
      // if (this._data) {
      //   chartWrapper?.free();
      // }
    },
  } as MarketPriceLinesSeriesWrapper);

  useLayoutEffect(() => {
    const currentRef = context.current;
    currentRef.data();

    return () => currentRef.free();
  }, []);

  useImperativeHandle(ref, () => context.current.data(), []);

  return <></>;
});
MarketPriceLinesSeries.displayName = 'MarketPriceLinesSeries';
