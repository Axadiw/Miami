import { Checkbox, Group, Input, NumberInput } from '@mantine/core';
import React, { useEffect } from 'react';
import { useSharedPositionContext } from '@/contexts/SharedPositionContext/SharedPositionContext';
import { useScaledPositionContext } from '@/app/scaled/contexts/ScaledPositionContext/ScaledPositionContext';
import { useScaledPositionDetailsValidators } from '@/app/scaled/hooks/useScaledPositionDetailsValidator/useScaledPositionDetailsValidators';

export interface SetScaledRangeProps {
  active: number;
}

export const SetScaledRange = (props: SetScaledRangeProps) => {
  const {
    lowerPrice,
    upperPrice,
    setUpperPrice,
    setLowerPrice,
    ordersCount,
    setOrdersCount,
    upperPriceAsCurrent,
    setUpperPriceAsCurrent,
  } = useScaledPositionContext();

  const { currentPrice } = useSharedPositionContext();
  const { active } = props;

  useEffect(() => {
    if (upperPriceAsCurrent === true) {
      setUpperPrice(currentPrice);
    } else if (upperPriceAsCurrent === false) {
      setLowerPrice(currentPrice);
    }
  }, [currentPrice, setLowerPrice, setUpperPrice, upperPriceAsCurrent]);

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
          <Checkbox
            disabled={active < 2}
            checked={upperPriceAsCurrent === true}
            onChange={(event) =>
              setUpperPriceAsCurrent(event.currentTarget.checked ? true : undefined)
            }
            label="Bind with current price"
          />
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
          <Checkbox
            disabled={active < 2}
            checked={upperPriceAsCurrent === false}
            onChange={(event) =>
              setUpperPriceAsCurrent(event.currentTarget.checked ? false : undefined)
            }
            label="Bind with current price"
          />
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
