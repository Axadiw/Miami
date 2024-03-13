import { Group, Input, NumberInput, SegmentedControl, Text } from '@mantine/core';
import React from 'react';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';
import { PriceTypeType } from '@/app/shared/components/positionCalculators/marketCalculator';
import { usePositionDetailsValidators } from '@/app/shared/hooks/usePositionDetailsValidators/usePositionDetailsValidators';

export const RiskManagementStep = () => {
  const {
    active,
    maxLoss,
    setMaxLoss,
    maxLossType,
    setMaxLossType,
    calculatedValues,
    slType,
    sl,
    setSl,
    setSlType,
  } = useMarketPageContext();

  const { maximumLossAbove0, slAbove0, slBelowOpen } = usePositionDetailsValidators();
  return (
    <>
      <Input.Wrapper label="Max loss:" size="xs">
        <Group>
          <NumberInput
            disabled={active < 2}
            w="100px"
            min={0}
            size="xs"
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
          <Text>
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
            size="xs"
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
