import { Button, Stack, Text } from '@mantine/core';
import React from 'react';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';
import { usePositionDetailsValidators } from '@/app/shared/hooks/usePositionDetailsValidators/usePositionDetailsValidators';
import { useCreateMarketPosition } from '@/api/useCreateMarketPosition';

export const ExecuteButton = () => {
  const {
    active,
    side,
    selectedAccountId,
    selectedSymbol,
    calculatedValues,
    comment,
    slToBreakEvenAtTp1,
    externalChartHelperURL,
  } = useMarketPageContext();
  const validators = usePositionDetailsValidators();
  useCreateMarketPosition;
  const { mutate } = useCreateMarketPosition();
  const actualErrors = Object.entries(validators)
    .map((v) => v[1])
    .filter((element) => element !== undefined);
  return (
    <Stack>
      <Button
        disabled={active < 4 || actualErrors.length > 0}
        onClick={() => {
          if (calculatedValues && selectedAccountId && selectedSymbol && comment) {
            mutate({
              side,
              accountId: +selectedAccountId,
              symbol: selectedSymbol,
              positionSize: calculatedValues.positionSize,
              takeProfits: [
                [calculatedValues.tp1Price, calculatedValues.tp1Percent],
                [calculatedValues.tp2Price, calculatedValues.tp2Percent],
                [calculatedValues.tp3Price, calculatedValues.tp3Percent],
              ],
              stopLoss: calculatedValues.slPrice,
              comment,
              moveSlToBreakevenAfterTp1: slToBreakEvenAtTp1,
              helperUrl: externalChartHelperURL,
            });
          }
        }}
      >
        Execute
      </Button>
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
