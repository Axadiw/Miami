'use client';

import { Center, Stack, Text, useMantineColorScheme } from '@mantine/core';
import Image from 'next/image';
import React from 'react';
import lightLogoImage from '@/public/logo-light.png';
import darkLogoImage from '@/public/logo-dark.png';

export default function DashboardPage() {
  const { colorScheme } = useMantineColorScheme();
  const isDarkTheme = colorScheme === 'dark';
  return (
    <Stack>
      <Text>
        Welcome to Miami Trade - risk aware trading platform
        <br />
      </Text>
      <Center>
        <Image src={isDarkTheme ? darkLogoImage : lightLogoImage} alt="logo" width={512} />
      </Center>
    </Stack>
  );
}
