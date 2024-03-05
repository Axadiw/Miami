import React, { forwardRef, useCallback, useState } from 'react';
import { ChartContainer } from '@/app/shared/components/chart/chartContainer';
import { ChartOptionsBase } from '@/vendor/lightweight-charts/src/model/chart-model';

export interface ChartComponentProps {
  updateSlAfterDragging: (newSl: number) => void;
  updateTP1AfterDragging: (newTP: number) => void;
  updateTP2AfterDragging: (newTP: number) => void;
  updateTP3AfterDragging: (newTP: number) => void;
  options: Partial<ChartOptionsBase>;
  children?: any;
}

export const ChartComponent = forwardRef((props: ChartComponentProps, ref) => {
  const [container, setContainer] = useState<HTMLDivElement | undefined>();
  const handleRef = useCallback((handRef: HTMLDivElement) => setContainer(handRef), []);
  return (
    <div ref={handleRef}>
      {container && <ChartContainer ref={ref} {...props} container={container} />}
    </div>
  );
});
