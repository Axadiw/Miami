import { Button, Group } from '@mantine/core';
import React, { useEffect } from 'react';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';

export const TimeframesSelector = () => {
  const { timeframes, selectedTimeframe, setSelectedTimeframe } = useMarketPageContext();
  useEffect(() => {
    if (timeframes && timeframes.timeframes.length > 0) {
      setSelectedTimeframe(timeframes.timeframes.includes('1h') ? '1h' : timeframes.timeframes[0]);
    }
  }, [setSelectedTimeframe, timeframes]);
  return (
    <Group>
      {timeframes &&
        timeframes.timeframes.map((timeframe) => (
          <Button
            key={`tf-${timeframe}`}
            variant={timeframe === selectedTimeframe ? 'filled' : 'default'}
            size="xs"
            onClick={() => {
              setSelectedTimeframe(timeframe);
            }}
          >
            {timeframe}
          </Button>
        ))}
    </Group>
  );
};
