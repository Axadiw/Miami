/* eslint-disable react/no-this-in-sfc */
import React, { forwardRef, useImperativeHandle, useLayoutEffect, useRef } from 'react';
import { createChart } from '@/vendor/lightweight-charts/src';
import { ChartContext, ChartWrapper } from '@/contexts/ChartContext/ChartContext';
import { ChartComponentProps } from '@/app/shared/components/chart/chartComponent';

interface ChartContainerProps extends ChartComponentProps {
  container: any;
}

export const ChartContainer = forwardRef((props: ChartContainerProps, ref) => {
  const {
    container,
    options,
    updateSlAfterDragging,
    updateTP1AfterDragging,
    updateTP2AfterDragging,
    updateTP3AfterDragging,
  } = props;

  const chartApiRef = useRef({
    chart() {
      if (!this._chart) {
        const chart = createChart(container, {
          ...options,
          width: container.clientWidth,
          height: 300,
        });

        chart.timeScale().applyOptions({
          rightOffset: 9,
          fixLeftEdge: true,
          timeVisible: true,
        });
        chart.subscribeCustomPriceLineDragged((params) => {
          switch (params.customPriceLine.options().title) {
            case 'SL': // TODO: move to const
              updateSlAfterDragging(params.customPriceLine.options().price);
              break;
            case 'TP1': // TODO: move to const
              updateTP1AfterDragging(params.customPriceLine.options().price);
              break;
            case 'TP2': // TODO: move to const
              updateTP2AfterDragging(params.customPriceLine.options().price);
              break;
            case 'TP3': // TODO: move to const
              updateTP3AfterDragging(params.customPriceLine.options().price);
              break;
          }
        });

        chart.timeScale().fitContent();
        this._chart = chart;
      }
      return this._chart;
    },
    free() {
      // if (this._chart) {
      //   this._chart.remove();
      // }
    },
  } as ChartWrapper);

  useLayoutEffect(() => {
    const currentRef = chartApiRef.current;
    const chart = currentRef.chart();

    const handleResize = () => {
      chart.applyOptions({
        width: container.clientWidth,
      });
    };

    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      // chart.remove();
    };
  }, [container.clientWidth]);

  useLayoutEffect(() => {
    const currentRef = chartApiRef.current;
    currentRef.chart().applyOptions(options);
  }, [options]);

  useLayoutEffect(() => {
    const currentRef = chartApiRef.current;
    currentRef.chart();
  }, []);

  useImperativeHandle(ref, () => chartApiRef.current.chart(), []);

  return (
    <ChartContext.Provider value={{ chartWrapper: chartApiRef.current }}>
      {props.children}
    </ChartContext.Provider>
  );
});
ChartContainer.displayName = 'ChartContainer';
