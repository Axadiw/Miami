import { Button, Center, Grid, SegmentedControl, Space } from '@mantine/core';
import React, { useEffect } from 'react';
import { useSharedPositionContext } from '@/contexts/SharedPositionContext/SharedPositionContext';

export const TimeframesSelector = () => {
  const { timeframes, selectedTimeframe, setSelectedTimeframe, chartAutoSize, setChartAutoSize } =
    useSharedPositionContext();
  useEffect(() => {
    if (timeframes && timeframes.timeframes.length > 0) {
      setSelectedTimeframe(timeframes.timeframes.includes('1h') ? '1h' : timeframes.timeframes[0]);
    }
  }, [setSelectedTimeframe, timeframes]);
  return (
    <Grid grow>
      <Grid.Col span={0}>
        <Space />
      </Grid.Col>
      <Grid.Col span={8}>
        <Center>
          {timeframes && (
            <SegmentedControl
              value={selectedTimeframe ?? undefined}
              onChange={(timeframe) => setSelectedTimeframe(timeframe)}
              data={timeframes.timeframes}
            />
          )}
        </Center>
      </Grid.Col>
      <Grid.Col span={1}>
        <Button
          variant={chartAutoSize ? 'filled' : 'default'}
          onClick={() => {
            setChartAutoSize(!chartAutoSize);
          }}
        >
          Autosize
        </Button>
      </Grid.Col>
    </Grid>
  );
};
