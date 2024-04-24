import { Group, Input, NumberInput, SegmentedControl, Text } from '@mantine/core';
import React, { ReactNode } from 'react';
import {
  MarketCalculatorResponse,
  PriceTypeType,
} from '@/app/shared/components/positionCalculators/marketCalculator';
import { useSharedPositionDetailsValidators } from '@/app/shared/hooks/useSharedPositionDetailsValidators/useSharedPositionDetailsValidators';
import { useSharedPositionContext } from '@/contexts/SharedPositionContext/SharedPositionContext';

export interface RiskManagementStepProps {
  calculatedValues?: MarketCalculatorResponse;
  children?: ReactNode;
  active: number;
}

export const RiskManagementStep = (props: RiskManagementStepProps) => {
  const { maxLoss, setMaxLoss, maxLossType, setMaxLossType, slType, sl, setSl, setSlType } =
    useSharedPositionContext();
  const { calculatedValues, active } = props;

  const largeRiskDetected = calculatedValues && calculatedValues.maxLossPercent > 80;

  const { maximumLossAbove0, slAbove0, slBelowOpen } =
    useSharedPositionDetailsValidators(calculatedValues);
  return (
    <>
      {props.children && props.children}
      <Input.Wrapper label="Max loss:" size="xs">
        <Group>
          <NumberInput
            disabled={active < 2}
            w="100px"
            min={0}
            size="md"
            value={maxLoss}
            onChange={setMaxLoss}
            error={maximumLossAbove0}
          />
          <SegmentedControl
            value={maxLossType}
            disabled={active < 2}
            onChange={(v) => setMaxLossType(v as PriceTypeType)}
            color={maxLossType === '%' ? 'yellow' : 'violet'}
            data={['%', '$']}
          />
          <Text
            c={largeRiskDetected ? 'red' : undefined}
            size={largeRiskDetected ? 'xl' : 'md'}
            fw={largeRiskDetected ? 800 : undefined}
          >
            {calculatedValues &&
              maxLoss &&
              maxLossType === '%' &&
              `$${calculatedValues.maxLossUSD.toFixed(2)}`}
            {calculatedValues &&
              maxLoss &&
              maxLossType === '$' &&
              `${calculatedValues.maxLossPercent.toFixed(2)}%`}
          </Text>
        </Group>
      </Input.Wrapper>
      <Input.Wrapper label="Stop loss" size="xs">
        <Group>
          <NumberInput
            disabled={active < 2}
            w="100px"
            min={0}
            max={slType === '%' ? 100 : undefined}
            size="md"
            value={sl}
            onChange={(v) => {
              setSl(v);
            }}
            error={slAbove0 ?? slBelowOpen}
          />
          <SegmentedControl
            disabled={active < 2}
            value={slType}
            color={slType === '%' ? 'yellow' : 'violet'}
            onChange={(v) => {
              setSlType(v as PriceTypeType);
            }}
            data={['%', '$']}
          />
          <Text>
            {calculatedValues && sl && slType === '%' && `$${calculatedValues.slPrice.toFixed(6)}`}
            {calculatedValues &&
              sl &&
              slType === '$' &&
              `${calculatedValues.slPercent.toFixed(2)}%`}
          </Text>
        </Group>
      </Input.Wrapper>

      {active > 2 && calculatedValues && (
        <Text>
          Position size: {calculatedValues.positionSize.toFixed(6)} ($
          {calculatedValues.positionSizeUSD.toFixed(2)})
        </Text>
      )}
    </>
  );
};
