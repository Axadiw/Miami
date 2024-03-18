import { Button, Center, List, Stack, Text, Transition } from '@mantine/core';
import React, { useState } from 'react';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';
import { usePositionDetailsValidators } from '@/app/shared/hooks/usePositionDetailsValidators/usePositionDetailsValidators';
import { useDataLayerContext } from '@/contexts/DataLayerContext/DataLayerContext';

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
    tp1Percent,
    tp2Percent,
    tp3Percent,
    setSl,
    setTp1,
    setTp2,
    setTp3,
    setTp1Type,
    setTp2Type,
    setTp3Type,
    setSlType,
    setMaxLossType,
    setExternalChartHelperURL,
    setSelectedSymbol,
    setMaxLoss,
    softStopLossTimeout,
    softStopLossEnabled,
  } = useMarketPageContext();
  const validators = usePositionDetailsValidators();
  const dataLayer = useDataLayerContext();
  const { mutateAsync, isPending, reset, error: createError } = dataLayer.useCreateMarketPosition();
  const actualErrors = Object.entries(validators)
    .map((v) => v[1])
    .filter((element) => element !== undefined);
  const [showButtonSuccess, setShowButtonSuccess] = useState<boolean>(false);

  return (
    <Stack>
      <Button
        disabled={active < 4 || actualErrors.length > 0}
        loading={isPending}
        onClick={async () => {
          try {
            if (calculatedValues && selectedAccountId && selectedSymbol && comment !== undefined) {
              reset();
              await mutateAsync({
                side,
                accountId: +selectedAccountId,
                symbol: selectedSymbol,
                positionSize: calculatedValues.positionSize,
                takeProfits: [
                  [calculatedValues.tp1Price, +(tp1Percent ?? 0)],
                  [calculatedValues.tp2Price, +(tp2Percent ?? 0)],
                  [calculatedValues.tp3Price, +(tp3Percent ?? 0)],
                ],
                stopLoss: calculatedValues.slPrice,
                softStopLossTimeout:
                  softStopLossEnabled && softStopLossTimeout ? +softStopLossTimeout : 0,
                comment,
                moveSlToBreakevenAfterTp1: slToBreakEvenAtTp1,
                helperUrl: externalChartHelperURL ?? '',
              });
              setSelectedSymbol(null);
              setMaxLoss('');
              setSl('');
              setTp1('');
              setTp2('');
              setTp3('');
              setTp1Type('%');
              setTp2Type('%');
              setTp3Type('%');
              setSlType('%');
              setMaxLossType('%');
              setExternalChartHelperURL('');
              setShowButtonSuccess(true);
              setTimeout(() => {
                setShowButtonSuccess(false);
              }, 2000);
            }
          } catch (e) {
            /* empty */
          }
        }}
      >
        Execute
      </Button>
      <Transition
        mounted={showButtonSuccess}
        transition="fade"
        duration={1000}
        timingFunction="ease"
      >
        {(styles) => (
          <Center>
            <Text style={styles}>Position created successfully!</Text>
          </Center>
        )}
      </Transition>
      <List c="red" size="xs">
        {actualErrors.map((e, i) => (
          <List.Item key={i}>{e}</List.Item>
        ))}
        {createError && <List.Item key="createError">{createError.message}</List.Item>}
      </List>
    </Stack>
  );
};
