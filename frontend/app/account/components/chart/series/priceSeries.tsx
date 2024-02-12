/* eslint-disable react/no-this-in-sfc */
import React, { forwardRef, useImperativeHandle, useLayoutEffect, useRef } from 'react';
import { ChartContext, PriceSeriesWrapper, useChartContext } from '@/contexts/ChartContext/ChartContext';

export const PriceSeries = forwardRef(
  (
    props: {
      children?: any;
    },
    ref
  ) => {
    const { chartWrapper } = useChartContext();

    const context = useRef({
      series() {
        if (!this._series) {
          const series = chartWrapper?.chart().addCandlestickSeries({
            priceFormat: { precision: 6, minMove: 0.000001 },
          });
          series?.priceScale().applyOptions({
            scaleMargins: {
              top: 0.01,
              bottom: 0.1,
            },
          });
          this._series = series;
        }
        return this._series;
      },
      free() {
        // if (this._series) {
        //   chartWrapper?.free();
        // }
      },
    } as PriceSeriesWrapper);

    useLayoutEffect(() => {
      const currentRef = context.current;
      currentRef.series();

      return () => currentRef.free();
    }, []);

    useImperativeHandle(ref, () => context.current.series(), []);

    return (
      <ChartContext.Provider
        value={{
          chartWrapper,
          priceSeriesWrapper: context.current,
        }}
      >
        {props.children}
      </ChartContext.Provider>
    );
  }
);
PriceSeries.displayName = 'PriceSeries';
