import { Button, Center, List, Stack, Text, Transition } from '@mantine/core';
import React, { useState } from 'react';
import { useSharedPositionDetailsValidators } from '@/app/shared/hooks/useSharedPositionDetailsValidators/useSharedPositionDetailsValidators';
import { useClearSharedPositionCreationFields } from '@/app/shared/hooks/useClearSharedPositionCreationFields/useClearSharedPositionCreationFields';
import { MarketCalculatorResponse } from '@/app/market/components/positionCalculators/marketCalculator';

export interface ExecuteButtonProps {
  additionalValidators?: [string, string | undefined][];
  calculatedValues?: MarketCalculatorResponse;
  createPositionAndCleanupForm: () => Promise<boolean>;
  isPending: boolean;
  error: Error | null;
  active: number;
}

export const ExecuteButton = (props: ExecuteButtonProps) => {
  const clearSharedFields = useClearSharedPositionCreationFields();
  const generalValidators = useSharedPositionDetailsValidators(props.calculatedValues);
  const actualErrors = [
    ...Object.entries(generalValidators),
    ...(props.additionalValidators ? props.additionalValidators : []),
  ]
    .map((v) => v[1])
    .filter((element) => element !== undefined);
  const [showButtonSuccess, setShowButtonSuccess] = useState<boolean>(false);

  return (
    <Stack>
      <Button
        disabled={props.active < 4 || actualErrors.length > 0}
        loading={props.isPending}
        onClick={async () => {
          if (await props.createPositionAndCleanupForm()) {
            clearSharedFields();
            setShowButtonSuccess(true);
            setTimeout(() => {
              setShowButtonSuccess(false);
            }, 2000);
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
        {props.error && <List.Item key="createError">{props.error.message}</List.Item>}
      </List>
    </Stack>
  );
};
