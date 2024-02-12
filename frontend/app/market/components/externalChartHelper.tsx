import { Group, Image, TextInput } from '@mantine/core';
import React from 'react';
import PrismaZoom from 'react-prismazoom';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';

export const ExternalChartHelper = () => {
  const { iframeURL, setIFrameURL } = useMarketPageContext();
  return (
    <>
      {iframeURL && (
        <Group h={300} style={{ overflow: 'hidden' }}>
          <PrismaZoom style={{ overflow: 'hidden' }}>
            <Image alt="Helper" src={iframeURL} height={300} style={{ overflow: 'hidden' }} />
          </PrismaZoom>
        </Group>
      )}
      <TextInput
        size="xs"
        value={iframeURL}
        onChange={(v) => setIFrameURL(v.currentTarget.value)}
        label="URL"
        placeholder="type URL"
      />
    </>
  );
};
