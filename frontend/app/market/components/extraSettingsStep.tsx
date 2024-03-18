import { Group, Input, NumberInput, Space, Switch, Textarea } from '@mantine/core';
import React from 'react';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';
import { usePositionDetailsValidators } from '@/app/shared/hooks/usePositionDetailsValidators/usePositionDetailsValidators';

export const ExtraSettingsStep = () => {
  const {
    slToBreakEvenAtTp1,
    setSlToBreakEvenAtTp1,
    active,
    comment,
    setComment,
    softStopLossEnabled,
    setSoftStopLossEnabled,
    softStopLossTimeout,
    setSoftStopLossTimeout,
  } = useMarketPageContext();

  const { softSlAbove0 } = usePositionDetailsValidators();

  return (
    <>
      <Switch
        disabled={active < 4}
        label="Move SL to breakeven at TP1"
        checked={slToBreakEvenAtTp1}
        onChange={(event) => setSlToBreakEvenAtTp1(event.currentTarget.checked)}
      />
      <Space h="md" />
      <Textarea
        disabled={active < 4}
        placeholder="Insert comment"
        value={comment}
        onChange={(event) => setComment(event.currentTarget.value)}
        autosize
        minRows={2}
        maxRows={4}
        error={comment && comment.length > 1000 ? 'Max 1000 chars' : undefined}
      />
      <Group>
        <Switch
          disabled={active < 4}
          label="Soft stop loss"
          checked={softStopLossEnabled}
          onChange={(event) => setSoftStopLossEnabled(event.currentTarget.checked)}
        />
        <Input.Wrapper label="Timeout (seconds)" size="xs">
          <Group>
            <NumberInput
              disabled={active < 4 || !softStopLossEnabled}
              w="100px"
              min={0}
              size="md"
              value={softStopLossTimeout}
              onChange={(v) => {
                setSoftStopLossTimeout(v);
              }}
              error={softSlAbove0}
            />
          </Group>
        </Input.Wrapper>
      </Group>
    </>
  );
};
