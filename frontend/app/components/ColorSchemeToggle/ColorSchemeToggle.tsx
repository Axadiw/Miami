'use client';
import { Text, Button, Group, useMantineColorScheme } from '@mantine/core';
import React from 'react';

export function ColorSchemeToggle() {
  const { setColorScheme } = useMantineColorScheme();

  return (
    <Group justify="center" mt="xl">
      <Text size={'xs'}>Theme:</Text>
      <Button size={'xs'} onClick={() => setColorScheme('light')}>
        Light
      </Button>
      <Button size={'xs'} onClick={() => setColorScheme('dark')}>
        Dark
      </Button>
      <Button size={'xs'} onClick={() => setColorScheme('auto')}>
        Auto
      </Button>
    </Group>
  );
}
