import { Button, Group, Input, NumberInput } from '@mantine/core';
import React from 'react';
import { useSharedPositionContext } from '@/contexts/SharedPositionContext/SharedPositionContext';
import { useScaledPositionContext } from '@/app/scaled/contexts/ScaledPositionContext/ScaledPositionContext';
import { useScaledPositionDetailsValidators } from '@/app/scaled/hooks/useScaledPositionDetailsValidator/useScaledPositionDetailsValidators';

export interface SetScaledRangeProps {
  active: number;
}

export const SetScaledRange = (props: SetScaledRangeProps) => {
  const { lowerPrice, upperPrice, setUpperPrice, setLowerPrice, ordersCount, setOrdersCount } =
    useScaledPositionContext();
  const { currentPrice } = useSharedPositionContext();
  const { active } = props;

  const {
    OrdersCountAbove2,
    RangeAboveCurrentPriceWhenShort,
    RangeBelowCurrentPriceWhenLong,
    UpperPriceAbove0,
    UpperAboveLower,
    LowerPriceAbove0,
    OrdersCountIsInteger,
  } = useScaledPositionDetailsValidators();

  return (
    <>
      <Input.Wrapper label="Upper:" size="xs">
        <Group>
          <NumberInput
            disabled={active < 2}
            w="100px"
            min={0}
            size="md"
            value={upperPrice}
            onChange={setUpperPrice}
            error={UpperAboveLower || UpperPriceAbove0 || RangeAboveCurrentPriceWhenShort}
          />
          <Button
            disabled={active < 2}
            size="xs"
            onClick={() => {
              setUpperPrice(currentPrice);
            }}
          >
            Set current price
          </Button>
        </Group>
      </Input.Wrapper>
      <Input.Wrapper label="Lower:" size="xs">
        <Group>
          <NumberInput
            disabled={active < 2}
            w="100px"
            min={0}
            size="md"
            value={lowerPrice}
            onChange={setLowerPrice}
            error={UpperAboveLower || LowerPriceAbove0 || RangeBelowCurrentPriceWhenLong}
          />
          <Button
            disabled={active < 2}
            size="xs"
            onClick={() => {
              setLowerPrice(currentPrice);
            }}
          >
            Set current price
          </Button>
        </Group>
      </Input.Wrapper>
      <Input.Wrapper label="Orders count:" size="xs">
        <Group>
          <NumberInput
            disabled={active < 2}
            w="100px"
            min={0}
            size="md"
            value={ordersCount}
            onChange={setOrdersCount}
            error={OrdersCountAbove2 || OrdersCountIsInteger}
          />
        </Group>
      </Input.Wrapper>
    </>
  );
};
