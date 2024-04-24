import { Group, Input, NumberInput, SegmentedControl, Slider, Stack, Text } from '@mantine/core';
import React from 'react';
import {
  MarketCalculatorResponse,
  PriceTypeType,
} from '@/app/shared/components/positionCalculators/marketCalculator';
import { useSharedPositionDetailsValidators } from '@/app/shared/hooks/useSharedPositionDetailsValidators/useSharedPositionDetailsValidators';
import { useSharedPositionContext } from '@/contexts/SharedPositionContext/SharedPositionContext';

export interface TakeProfitsStepProps {
  calculatedValues?: MarketCalculatorResponse;
  active: number;
}

export const TakeProfitsStep = (props: TakeProfitsStepProps) => {
  const {
    tp1,
    tp1Percent,
    setTp1,
    setTp1Type,
    tp2,
    tp2Percent,
    setTp2,
    setTp2Type,
    tp3,
    tp3Percent,
    setTp3,
    setTp3Type,
    tp1Type,
    tp2Type,
    tp3Type,
    setTp1Percent,
    setTp2Percent,
    setTp3Percent,
  } = useSharedPositionContext();

  const { calculatedValues, active } = props;

  const {
    tp1Above0,
    tp2Above0,
    tp3Above0,
    tp1AboveOpen,
    tp2AboveTp1,
    tp3AboveTp2,
    tpVolumesAddTo100,
  } = useSharedPositionDetailsValidators(calculatedValues);
  return (
    <>
      <Group>
        <Input.Wrapper label="Take profit 1:" size="xs">
          <Group>
            <NumberInput
              disabled={active < 3}
              w="100px"
              min={0}
              size="md"
              value={tp1}
              onChange={setTp1}
              error={tp1Above0 ?? tp1AboveOpen}
            />
            <SegmentedControl
              disabled={active < 3}
              value={tp1Type}
              onChange={(v) => setTp1Type(v as PriceTypeType)}
              color={tp1Type === '%' ? 'yellow' : 'violet'}
              data={['%', '$']}
            />
            <Text>
              {calculatedValues &&
                tp1 &&
                tp1Type === '%' &&
                `$${calculatedValues.tp1Price.toFixed(6)}`}
              {calculatedValues &&
                tp1 &&
                tp1Type === '$' &&
                `(${calculatedValues.tp1Percent.toFixed(2)}%)`}
            </Text>
          </Group>
        </Input.Wrapper>
        <Input.Wrapper label="Volume" size="xs">
          <Group>
            <Stack>
              <NumberInput
                disabled={active < 3}
                w="70px"
                min={0}
                max={100}
                size="md"
                value={tp1Percent}
                onChange={setTp1Percent}
                error={tpVolumesAddTo100}
              />
              <Slider
                color="blue"
                disabled={active < 3}
                value={tp1Percent as number}
                onChange={setTp1Percent}
              />
            </Stack>
            <Text c="green">
              {calculatedValues &&
                tp1 &&
                tp1Percent &&
                `$ ${calculatedValues.tp1USDReward.toFixed(2)}`}
            </Text>
          </Group>
        </Input.Wrapper>
      </Group>

      <Group>
        <Input.Wrapper label="Take profit 2:" size="xs">
          <Group>
            <NumberInput
              disabled={active < 3}
              w="100px"
              min={0}
              size="md"
              value={tp2}
              onChange={setTp2}
              error={tp2Above0 ?? tp2AboveTp1}
            />
            <SegmentedControl
              disabled={active < 3}
              value={tp2Type}
              color={tp2Type === '%' ? 'yellow' : 'violet'}
              onChange={(v) => setTp2Type(v as PriceTypeType)}
              data={['%', '$']}
            />
            <Text>
              {calculatedValues &&
                tp2 &&
                tp2Type === '%' &&
                `$${calculatedValues.tp2Price.toFixed(6)}`}
              {calculatedValues &&
                tp2 &&
                tp2Type === '$' &&
                `(${calculatedValues.tp2Percent.toFixed(2)}%)`}
            </Text>
          </Group>
        </Input.Wrapper>
        <Input.Wrapper label="Volume" size="xs">
          <Group>
            <Stack>
              <NumberInput
                disabled={active < 3}
                w="70px"
                min={0}
                max={100}
                size="md"
                value={tp2Percent}
                onChange={setTp2Percent}
                error={tpVolumesAddTo100}
              />
              <Slider
                color="blue"
                disabled={active < 3}
                value={tp2Percent as number}
                onChange={setTp2Percent}
              />
            </Stack>

            <Text c="green">
              {calculatedValues &&
                tp2 &&
                tp2Percent &&
                `$ ${calculatedValues.tp2USDReward.toFixed(2)}`}
            </Text>
          </Group>
        </Input.Wrapper>
      </Group>
      <Group>
        <Input.Wrapper label="Take profit 3:" size="xs">
          <Group>
            <NumberInput
              disabled={active < 3}
              w="100px"
              size="md"
              min={0}
              value={tp3}
              onChange={setTp3}
              error={tp3Above0 ?? tp3AboveTp2}
            />
            <SegmentedControl
              disabled={active < 3}
              value={tp3Type}
              color={tp3Type === '%' ? 'yellow' : 'violet'}
              onChange={(v) => setTp3Type(v as PriceTypeType)}
              data={['%', '$']}
            />
            <Text>
              {calculatedValues &&
                tp3 &&
                tp3Type === '%' &&
                `$${calculatedValues.tp3Price.toFixed(6)}`}
              {calculatedValues &&
                tp3 &&
                tp3Type === '$' &&
                `(${calculatedValues.tp3Percent.toFixed(2)}%)`}
            </Text>
          </Group>
        </Input.Wrapper>
        <Group>
          <Input.Wrapper label="Volume" size="xs">
            <Stack>
              <NumberInput
                disabled={active < 3}
                w="70px"
                size="md"
                min={0}
                max={100}
                value={tp3Percent}
                onChange={setTp3Percent}
                error={tpVolumesAddTo100}
              />
              <Slider
                color="blue"
                disabled={active < 3}
                value={tp3Percent as number}
                onChange={setTp3Percent}
              />
            </Stack>
          </Input.Wrapper>
          <Text c="green">
            {calculatedValues &&
              tp3 &&
              tp3Percent &&
              `$ ${calculatedValues.tp3USDReward.toFixed(2)}`}
          </Text>
        </Group>
      </Group>
    </>
  );
};
