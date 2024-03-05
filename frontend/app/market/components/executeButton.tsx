import { Button, Stack, Text } from '@mantine/core';
import React from 'react';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';
import { usePositionDetailsValidators } from '@/app/shared/hooks/usePositionDetailsValidators/usePositionDetailsValidators';

export const ExecuteButton = () => {
  const { active } = useMarketPageContext();
  const validators = usePositionDetailsValidators();
  const actualErrors = Object.entries(validators)
    .map((v) => v[1])
    .filter((element) => element !== undefined);
  return (
    <Stack>
      <Button disabled={active < 4 || actualErrors.length > 0}>Execute</Button>
      <Text c="red" size="xs">
        <ul>
          {actualErrors.map((e) => (
            <li>{e}</li>
          ))}
        </ul>
      </Text>
    </Stack>
  );
};
