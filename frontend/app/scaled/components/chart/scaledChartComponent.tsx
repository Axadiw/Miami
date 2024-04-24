import React, { forwardRef, useCallback, useState } from 'react';
import { ChartOptionsBase } from '@/vendor/lightweight-charts/src/model/chart-model';
import { ScaledChartContainer } from '@/app/scaled/components/chart/scaledChartContainer';

export interface ScaledChartComponentProps {
  updateSlAfterDragging: (newSl: number) => void;
  updateTP1AfterDragging: (newTP: number) => void;
  updateTP2AfterDragging: (newTP: number) => void;
  updateTP3AfterDragging: (newTP: number) => void;
  updateUpperAfterDragging: (newUpper: number) => void;
  updateLowerAfterDragging: (newLower: number) => void;
  options: Partial<ChartOptionsBase>;
  children?: any;
}

export const ScaledChartComponent = forwardRef((props: ScaledChartComponentProps, ref) => {
  const [container, setContainer] = useState<HTMLDivElement | undefined>();
  const handleRef = useCallback((handRef: HTMLDivElement) => setContainer(handRef), []);
  return (
    <div ref={handleRef}>
      {container && <ScaledChartContainer ref={ref} {...props} container={container} />}
    </div>
  );
});
