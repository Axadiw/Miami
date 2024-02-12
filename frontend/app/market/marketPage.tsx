'use client';

import { Group, NumberFormatter, SimpleGrid, Space, Stack, Text, Timeline } from '@mantine/core';
import React from 'react';
import {
  IconNumber0,
  IconNumber1,
  IconNumber2,
  IconNumber3,
  IconNumber4,
} from '@tabler/icons-react';
import { SideSelectionStep } from '@/app/market/components/sideSelectionStep';
import { SelectSymbolStep } from './components/selectSymbolStep';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';
import { RiskManagementStep } from './components/riskManagementStep';
import { TakeProfitsStep } from './components/takeProfitsStep';
import { MarketChart } from './components/marketChart';
import { TimeframesSelector } from '@/app/market/components/timeframesSelector';
import { ExternalChartHelper } from '@/app/market/components/externalChartHelper';
import { ExecuteButton } from '@/app/market/components/executeButton';
import { ExtraSettingsStep } from '@/app/market/components/extraSettingsStep';

export default function MarketPage() {
  const { accountBalance, active } = useMarketPageContext();

  return (
    <SimpleGrid cols={{ base: 1, sm: 2 }}>
      <Stack>
        <Group>
          <Text>Balance:</Text>
          <NumberFormatter prefix="$ " value={accountBalance} thousandSeparator />
        </Group>
        <Timeline active={active} bulletSize={24} lineWidth={2}>
          <Timeline.Item bullet={<IconNumber0 size={20} />}>
            <SideSelectionStep />
          </Timeline.Item>
          <Timeline.Item bullet={<IconNumber1 size={20} />}>
            <SelectSymbolStep />
          </Timeline.Item>
          <Timeline.Item bullet={<IconNumber2 size={20} />}>
            <RiskManagementStep />
          </Timeline.Item>
          <Timeline.Item bullet={<IconNumber3 size={20} />}>
            <TakeProfitsStep />
          </Timeline.Item>
          <Timeline.Item bullet={<IconNumber4 size={20} />}>
            <ExtraSettingsStep />
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
    </SimpleGrid>
  );
}
