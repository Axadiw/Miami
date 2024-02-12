'use client';

import { Group, NumberFormatter, Space, Stack, Text, Timeline } from '@mantine/core';
import React from 'react';
import {
  IconNumber0,
  IconNumber1,
  IconNumber2,
  IconNumber3,
  IconNumber4,
} from '@tabler/icons-react';
import { Step0 } from '@/app/market/components/step0';
import { Step1 } from './components/step1';
import {
  MarketPageContextProvider,
  useMarketPageContext,
} from '@/contexts/MarketPageContext/MarketPageContext';
import { Step2 } from './components/step2';
import { Step3 } from './components/step3';
import { Step4 } from '@/app/market/components/step4';
import { MarketChart } from './components/marketChart';
import { TimeframesSelector } from '@/app/market/components/timeframesSelector';
import { ExternalChartHelper } from '@/app/market/components/externalChartHelper';
import { ExecuteButton } from '@/app/market/components/executeButton';

export default function MarketPage() {
  const { accountBalance, active } = useMarketPageContext();

  return (
    <MarketPageContextProvider>
      <Stack>
        <Group grow align="flex-start">
          <Stack>
            <Group>
              <Text>Balance:</Text>
              <NumberFormatter prefix="$ " value={`${accountBalance}`} thousandSeparator />
            </Group>
            <Timeline active={active} bulletSize={24} lineWidth={2}>
              <Timeline.Item bullet={<IconNumber0 size={20} />}>
                <Step0 />
              </Timeline.Item>
              <Timeline.Item bullet={<IconNumber1 size={20} />}>
                <Step1 />
              </Timeline.Item>
              <Timeline.Item bullet={<IconNumber2 size={20} />}>
                <Step2 />
              </Timeline.Item>
              <Timeline.Item bullet={<IconNumber3 size={20} />}>
                <Step3 />
              </Timeline.Item>
              <Timeline.Item bullet={<IconNumber4 size={20} />}>
                <Step4 />
              </Timeline.Item>
            </Timeline>
            <Space h="md" />
          </Stack>

          <Stack>
            <Stack>
              <MarketChart />
              <TimeframesSelector />
              <ExternalChartHelper />
            </Stack>
            <Space h="md" />
            <ExecuteButton />
          </Stack>
        </Group>
      </Stack>
    </MarketPageContextProvider>
  );
}
