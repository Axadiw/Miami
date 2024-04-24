import React, { forwardRef, useCallback, useState } from 'react';
import { ChartOptionsBase } from '@/vendor/lightweight-charts/src/model/chart-model';
import { LimitChartContainer } from '@/app/limit/components/chart/limitChartContainer';

export interface LimitChartComponentProps {
  updateSlAfterDragging: (newSl: number) => void;
  updateTP1AfterDragging: (newTP: number) => void;
  updateTP2AfterDragging: (newTP: number) => void;
  updateTP3AfterDragging: (newTP: number) => void;
  updateLimitAfterDragging: (newLimit: number) => void;
  options: Partial<ChartOptionsBase>;
  children?: any;
}

export const LimitChartComponent = forwardRef((props: LimitChartComponentProps, ref) => {
  const [container, setContainer] = useState<HTMLDivElement | undefined>();
  const handleRef = useCallback((handRef: HTMLDivElement) => setContainer(handRef), []);
  return (
    <div ref={handleRef}>
      {container && <LimitChartContainer ref={ref} {...props} container={container} />}
    </div>
  );
});
