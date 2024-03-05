import { Group, SegmentedControl } from '@mantine/core';
import React from 'react';
import { Side } from '@/app/shared/components/positionCalculators/marketCalculator';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';

export const SideSelectionStep = () => {
  const { side, setSide } = useMarketPageContext();
  return (
    <Group>
      <SegmentedControl
        onChange={(v) => setSide(v as Side)}
        value={side}
        color={side === 'Long' ? 'green' : 'red'}
        data={['Long', 'Short']}
      />
    </Group>
  );
};
