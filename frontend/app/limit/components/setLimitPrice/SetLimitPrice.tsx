import { Button, Group, Input, NumberInput } from '@mantine/core';
import React from 'react';
import { useLimitPositionContext } from '@/app/limit/contexts/LimitPositionContext/LimitPositionContext';
import { useLimitPositionDetailsValidators } from '@/app/limit/hooks/useLimitPositionDetailsValidator/useLimitPositionDetailsValidators';
import { useSharedPositionContext } from '@/contexts/SharedPositionContext/SharedPositionContext';

export interface SetLimitPriceProps {
  active: number;
}

export const SetLimitPrice = (props: SetLimitPriceProps) => {
  const { limitPrice, setLimitPrice } = useLimitPositionContext();
  const { currentPrice } = useSharedPositionContext();
  const { active } = props;

  const {
    limitPriceAbove0,
    limitPriceBelowCurrentPriceWhenLong,
    limitPriceAboveCurrentPriceWhenShort,
  } = useLimitPositionDetailsValidators();

  return (
    <>
      <Input.Wrapper label="Price:" size="xs">
        <Group>
          <NumberInput
            disabled={active < 2}
            w="100px"
            min={0}
            size="md"
            value={limitPrice}
            onChange={setLimitPrice}
            error={
              limitPriceAbove0 ||
              limitPriceBelowCurrentPriceWhenLong ||
              limitPriceAboveCurrentPriceWhenShort
            }
          />
          <Button
            disabled={active < 2}
            size="xs"
            onClick={() => {
              setLimitPrice(currentPrice);
            }}
          >
            Set current price
          </Button>
        </Group>
      </Input.Wrapper>
    </>
  );
};
