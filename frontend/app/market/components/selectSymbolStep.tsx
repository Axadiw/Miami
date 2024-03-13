import { IconSearch } from '@tabler/icons-react';
import { Button, Group, rem, Text } from '@mantine/core';
import React from 'react';
import { spotlight, Spotlight } from '@mantine/spotlight';
import { useMarketPageContext } from '@/contexts/MarketPageContext/MarketPageContext';

export const SelectSymbolStep = () => {
  const { active, fetchSymbolsSuccess, symbols, setSelectedSymbol, selectedSymbol, currentPrice } =
    useMarketPageContext();
  const symbolsList = symbols?.symbols ?? [];
  return (
    <>
      {fetchSymbolsSuccess && (
        <>
          <Group>
            <Button disabled={active < 1} size="xs" onClick={spotlight.open}>
              Pick symbol
            </Button>
            <Spotlight
              actions={symbolsList?.map((value, index) => ({
                id: `symbol-${index}`,
                label: `${value}\n`,
                onClick: () => {
                  setSelectedSymbol(value);
                },
              }))}
              nothingFound="Nothing found..."
              highlightQuery
              scrollable
              searchProps={{
                leftSection: (
                  <IconSearch style={{ width: rem(20), height: rem(20) }} stroke={1.5} />
                ),
                placeholder: 'Select symbol...',
              }}
            />
          </Group>
        </>
      )}
      {selectedSymbol && <Text>Selected {selectedSymbol}</Text>}
      {currentPrice >= 0 && <Text>Current price: $ {currentPrice}</Text>}
    </>
  );
};
