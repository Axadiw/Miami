'use client';

import { SimpleGrid, Space, Stack, Timeline } from '@mantine/core';
import React from 'react';
import {
  IconNumber0,
  IconNumber1,
  IconNumber2,
  IconNumber3,
  IconNumber4,
} from '@tabler/icons-react';
import { useSharedPositionContext } from '@/contexts/SharedPositionContext/SharedPositionContext';
import { SetLimitPrice } from '@/app/limit/components/setLimitPrice/SetLimitPrice';
import { AccountAndSideSelectionStep } from '@/app/shared/components/positionsManagement/accountAndSideSelectionStep';
import { SelectSymbolStep } from '@/app/shared/components/positionsManagement/selectSymbolStep';
import { RiskManagementStep } from '@/app/shared/components/positionsManagement/riskManagementStep';
import { TakeProfitsStep } from '@/app/shared/components/positionsManagement/takeProfitsStep';
import { ExtraSettingsStep } from '@/app/shared/components/positionsManagement/extraSettingsStep';
import { TimeframesSelector } from '@/app/shared/components/positionsManagement/timeframesSelector';
import { ExternalChartHelper } from '@/app/shared/components/positionsManagement/externalChartHelper';
import { ExecuteButton } from '@/app/shared/components/positionsManagement/executeButton';
import { useDataLayerContext } from '@/contexts/DataLayerContext/DataLayerContext';
import { useLimitPositionContext } from '@/app/limit/contexts/LimitPositionContext/LimitPositionContext';
import { useLimitPositionDetailsValidators } from '@/app/limit/hooks/useLimitPositionDetailsValidator/useLimitPositionDetailsValidators';
import { LimitChart } from '@/app/limit/components/chart/limitChart';

export default function LimitPage() {
  const {
    side,
    selectedAccountId,
    selectedSymbol,
    comment,
    slToBreakEvenAtTp1,
    externalChartHelperURL,
    tp1Percent,
    tp2Percent,
    tp3Percent,
    softStopLossTimeout,
    softStopLossEnabled,
  } = useSharedPositionContext();
  const { limitPrice, calculatedValues, active, setLimitPrice } = useLimitPositionContext();

  const limitValidators = useLimitPositionDetailsValidators();

  const dataLayer = useDataLayerContext();
  const { mutateAsync, isPending, reset, error: createError } = dataLayer.useCreateLimitPosition();

  return (
    <SimpleGrid cols={{ base: 1, sm: 2 }}>
      <Stack>
        <Timeline active={active} bulletSize={24} lineWidth={2}>
          <Timeline.Item bullet={<IconNumber0 size={20} />}>
            <AccountAndSideSelectionStep />
          </Timeline.Item>
          <Timeline.Item bullet={<IconNumber1 size={20} />}>
            <SelectSymbolStep active={active} />
          </Timeline.Item>
          <Timeline.Item bullet={<IconNumber2 size={20} />}>
            <RiskManagementStep calculatedValues={calculatedValues} active={active}>
              <SetLimitPrice active={active} />
            </RiskManagementStep>
          </Timeline.Item>
          <Timeline.Item bullet={<IconNumber3 size={20} />}>
            <TakeProfitsStep calculatedValues={calculatedValues} active={active} />
          </Timeline.Item>
          <Timeline.Item bullet={<IconNumber4 size={20} />}>
            <ExtraSettingsStep calculatedValues={calculatedValues} active={active} />
          </Timeline.Item>
        </Timeline>
        <Space h="md" />
      </Stack>

      <Stack>
        <Stack>
          {selectedSymbol && (
            <>
              <LimitChart calculatedValues={calculatedValues} />
              <TimeframesSelector />
            </>
          )}
          <ExternalChartHelper />
        </Stack>
        <Space h="md" />
        <ExecuteButton
          active={active}
          isPending={isPending}
          error={createError}
          additionalValidators={Object.entries(limitValidators)}
          createPositionAndCleanupForm={async () => {
            try {
              if (
                calculatedValues &&
                selectedAccountId &&
                selectedSymbol &&
                comment !== undefined
              ) {
                reset();
                await mutateAsync({
                  side,
                  accountId: +selectedAccountId,
                  symbol: selectedSymbol,
                  positionSize: calculatedValues.positionSize,
                  takeProfits: [
                    [calculatedValues.tp1Price, +(tp1Percent ?? 0)],
                    [calculatedValues.tp2Price, +(tp2Percent ?? 0)],
                    [calculatedValues.tp3Price, +(tp3Percent ?? 0)],
                  ],
                  stopLoss: calculatedValues.slPrice,
                  softStopLossTimeout:
                    softStopLossEnabled && softStopLossTimeout ? +softStopLossTimeout : 0,
                  comment,
                  moveSlToBreakevenAfterTp1: slToBreakEvenAtTp1,
                  helperUrl: externalChartHelperURL ?? '',
                  limitPrice: Number(limitPrice),
                });
                setLimitPrice(undefined);
                return true;
              }
            } catch (e) {
              /* empty */
            }
            return Promise.resolve(false);
          }}
        />
      </Stack>
    </SimpleGrid>
  );
}
