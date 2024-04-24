/* eslint-disable react/no-this-in-sfc */
import {
  forwardRef,
  useEffect,
  useImperativeHandle,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import { useChartContext } from '@/contexts/ChartContext/ChartContext';
import { LineWidth } from '@/vendor/lightweight-charts/src/renderers/draw-line';
import { ScaledPriceLinesSeriesWrapper } from '@/app/scaled/types';
import { useScaledPositionContext } from '@/app/scaled/contexts/ScaledPositionContext/ScaledPositionContext';
import { IPriceLine } from '@/vendor/lightweight-charts/src/api/iprice-line';

interface ScaledPriceLineSeriesProps {}

export const ScaledPriceLinesSeries = forwardRef((props: ScaledPriceLineSeriesProps, ref) => {
  const { chartWrapper, priceSeriesWrapper } = useChartContext();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [midLines, setMidLines] = useState<IPriceLine[]>([]);
  const commonOptions = useMemo(
    () => ({
      price: 0,
      lineWidth: 1 as LineWidth,
      lineStyle: 2,
      axisLabelVisible: true,
      color: '#26a69a',
      draggable: true,
      lineVisible: false,
    }),
    []
  );
  const { upperPrice, lowerPrice, ordersCount } = useScaledPositionContext();

  useEffect(() => {
    if (upperPrice && lowerPrice && ordersCount && priceSeriesWrapper) {
      const length = Math.abs(Number(upperPrice) - Number(lowerPrice));
      const step = length / (Number(ordersCount) - 1);

      const levels: number[] = [];
      if (Number(ordersCount) > 2) {
        // eslint-disable-next-line no-plusplus
        for (let i = 1; i < Number(ordersCount) - 1; i++) {
          levels.push(Number(lowerPrice) + i * step);
        }
      }

      setMidLines((prevState) => {
        prevState.forEach((line) => {
          priceSeriesWrapper.series().removePriceLine(line);
        });
        return levels.map((price) =>
          priceSeriesWrapper.series().createPriceLine({
            ...commonOptions,
            draggable: false,
            lineVisible: true,
            axisLabelVisible: false,
            color: '#ffd966',
            price,
          })
        );
      });
    }
  }, [commonOptions, lowerPrice, ordersCount, priceSeriesWrapper, upperPrice]);

  const context = useRef({
    data() {
      if (!this._data && priceSeriesWrapper && chartWrapper?.chart()) {
        const lines = {
          upper: priceSeriesWrapper?.series().createPriceLine({
            ...commonOptions,
            title: 'Upper',
            color: '#ffd966',
          }),
          lower: priceSeriesWrapper?.series().createPriceLine({
            ...commonOptions,
            title: 'Lower',
            color: '#ffd966',
          }),
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
    free() {},
  } as ScaledPriceLinesSeriesWrapper);

  useLayoutEffect(() => {
    const currentRef = context.current;
    currentRef.data();

    return () => currentRef.free();
  }, []);

  useImperativeHandle(ref, () => context.current.data(), []);

  return <></>;
});
ScaledPriceLinesSeries.displayName = 'ScaledPriceLinesSeries';
