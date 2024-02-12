import { Switch } from '@mantine/core';
import React from 'react';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';

export const Step4 = () => {
  const { slToBreakEvenAtTp1, setSlToBreakEvenAtTp1, active } = useMarketPageContext();
  return (
    <>
      <Switch
        disabled={active < 4}
        label="Move SL to breakeven at TP1"
        checked={slToBreakEvenAtTp1}
        onChange={(event) => setSlToBreakEvenAtTp1(event.currentTarget.checked)}
      />
    </>
  );
};
