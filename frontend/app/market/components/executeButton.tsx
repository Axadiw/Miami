import { Button } from '@mantine/core';
import React from 'react';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';

export const ExecuteButton = () => {
  const { active } = useMarketPageContext();
  return <Button disabled={active < 4}>Execute</Button>;
};
