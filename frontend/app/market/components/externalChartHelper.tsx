import { Group, Image, TextInput } from '@mantine/core';
import React from 'react';
import PrismaZoom from 'react-prismazoom';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';

export const ExternalChartHelper = () => {
  const { externalChartHelperURL, setExternalChartHelperURL } = useMarketPageContext();
  return (
    <>
      {externalChartHelperURL && (
        <Group h={300} style={{ overflow: 'hidden' }}>
          <PrismaZoom>
            <Image alt="Helper" src={externalChartHelperURL} height={300} fit="contain" />
          </PrismaZoom>
        </Group>
      )}
      <TextInput
        size="xs"
        w="100%"
        value={externalChartHelperURL}
        onChange={(v) => setExternalChartHelperURL(v.currentTarget.value)}
        label="URL for external chart (double click to zoom)"
        placeholder="type URL"
      />
    </>
  );
};
