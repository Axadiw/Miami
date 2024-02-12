/* eslint-disable react/no-this-in-sfc */
import React, { forwardRef, useImperativeHandle, useLayoutEffect, useRef } from 'react';
import {
  ChartContext,
  useChartContext,
  VolumeSeriesWrapper,
} from '@/contexts/ChartContext/ChartContext';
import { SeriesProps } from '@/app/account/components/chart/series/common';

export const VolumeSeries = forwardRef((props: SeriesProps, ref) => {
  const { chartWrapper } = useChartContext();

  const context = useRef({
    series() {
      if (!this._series) {
        const { data } = props;
        const series = chartWrapper?.chart().addHistogramSeries({
          priceFormat: {
            type: 'volume',
          },
          lastValueVisible: false,
          priceScaleId: '',
        });
        series?.priceScale().applyOptions({
          scaleMargins: {
            top: 0.9,
            bottom: 0,
          },
        });
        series?.setData(data);

        this._series = series;
      }
      return this._series;
    },
    free() {
      if (this._series) {
        chartWrapper?.free();
      }
    },
  } as VolumeSeriesWrapper);

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
        volumeSeriesWrapper: context.current,
      }}
    >
      {props.children}
    </ChartContext.Provider>
  );
});
VolumeSeries.displayName = 'VolumeSeries';
