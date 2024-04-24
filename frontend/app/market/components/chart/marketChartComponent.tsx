import React, { forwardRef, useCallback, useState } from 'react';
import { MarketChartContainer } from '@/app/market/components/chart/marketChartContainer';
import { ChartOptionsBase } from '@/vendor/lightweight-charts/src/model/chart-model';

export interface MarketChartComponentProps {
  updateSlAfterDragging: (newSl: number) => void;
  updateTP1AfterDragging: (newTP: number) => void;
  updateTP2AfterDragging: (newTP: number) => void;
  updateTP3AfterDragging: (newTP: number) => void;
  options: Partial<ChartOptionsBase>;
  children?: any;
}

export const MarketChartComponent = forwardRef((props: MarketChartComponentProps, ref) => {
  const [container, setContainer] = useState<HTMLDivElement | undefined>();
  const handleRef = useCallback((handRef: HTMLDivElement) => setContainer(handRef), []);
  return (
    <div ref={handleRef}>
      {container && <MarketChartContainer ref={ref} {...props} container={container} />}
    </div>
  );
});
