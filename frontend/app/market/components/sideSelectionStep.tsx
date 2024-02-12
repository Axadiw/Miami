import { Group, SegmentedControl } from '@mantine/core';
import React from 'react';
import { Side } from '@/app/account/components/positionCalculators/marketCalculator';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';

export const SideSelectionStep = () => {
  const { side, setSide } = useMarketPageContext();
  return (
    <Group>
      <SegmentedControl
        onChange={(v) => setSide(v as Side)}
        value={side}
        color={side === 'Buy' ? 'green' : 'red'}
        data={['Buy', 'Sell']}
      />
    </Group>
  );
};
