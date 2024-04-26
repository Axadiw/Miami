import { ActionIcon, Checkbox, Group, Input, NumberInput, Stack } from '@mantine/core';
import React, { useEffect } from 'react';
import { IconRefresh } from '@tabler/icons-react';
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

  const { currentPrice, side } = useSharedPositionContext();
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
    <Stack>
      <Input.Wrapper label="Upper:" size="xs">
        <Group>
          <NumberInput
            disabled={active < 2}
            w="100px"
            min={0}
            size="md"
            value={upperPrice}
            onChange={(newPrice) => {
              setUpperPriceAsCurrent((prevState) => (prevState === true ? undefined : prevState));
              setUpperPrice(newPrice);
            }}
            error={UpperAboveLower || UpperPriceAbove0 || RangeAboveCurrentPriceWhenShort}
          />
          <Checkbox
            disabled={active < 2 || side === 'Short'}
            checked={upperPriceAsCurrent === true}
            onChange={(event) =>
              setUpperPriceAsCurrent(event.currentTarget.checked ? true : undefined)
            }
            label="Bind with current price"
          />
        </Group>
      </Input.Wrapper>
      <ActionIcon
        variant="default"
        display={UpperAboveLower !== undefined ? 'inline' : 'none'}
        size="md"
        radius="md"
        aria-label="Reverse"
        onClick={() => {
          const tmp = upperPrice;
          setUpperPrice(lowerPrice);
          setLowerPrice(tmp);
        }}
      >
        <IconRefresh style={{ width: '70%', height: '70%' }} stroke={1.5} />
      </ActionIcon>

      <Input.Wrapper label="Lower:" size="xs">
        <Group>
          <NumberInput
            disabled={active < 2}
            w="100px"
            min={0}
            size="md"
            value={lowerPrice}
            onChange={(newPrice) => {
              setUpperPriceAsCurrent((prevState) => (prevState === false ? undefined : prevState));
              setLowerPrice(newPrice);
            }}
            error={UpperAboveLower || LowerPriceAbove0 || RangeBelowCurrentPriceWhenLong}
          />
          <Checkbox
            disabled={active < 2 || side === 'Long'}
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
    </Stack>
  );
};
