import { Space, Switch, Textarea } from '@mantine/core';
import React from 'react';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';

export const ExtraSettingsStep = () => {
  const { slToBreakEvenAtTp1, setSlToBreakEvenAtTp1, active, comment, setComment } =
    useMarketPageContext();
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
    </>
  );
};
