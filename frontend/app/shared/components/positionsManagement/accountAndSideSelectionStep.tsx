import {
  Combobox,
  Group,
  Input,
  InputBase,
  NumberFormatter,
  SegmentedControl,
  Stack,
  Text,
  useCombobox,
} from '@mantine/core';
import React, { useEffect } from 'react';
import { Side } from '@/app/shared/components/positionCalculators/marketCalculator';
import { useDataLayerContext } from '@/contexts/DataLayerContext/DataLayerContext';
import { useSharedPositionContext } from '@/contexts/SharedPositionContext/SharedPositionContext';

export const AccountAndSideSelectionStep = () => {
  const { side, setSide, setSelectedAccountId, accountBalance, selectedAccountId } =
    useSharedPositionContext();

  const dataLayer = useDataLayerContext();
  const { isFetching: isBalanceLoading } = dataLayer.useGetAccountBalance({
    accountId: selectedAccountId,
  });

  const { data: existingAccounts } = dataLayer.useListExchangeAccounts();

  useEffect(() => {
    if (existingAccounts?.accounts && existingAccounts?.accounts.length > 0) {
      setSelectedAccountId(existingAccounts?.accounts[0].id);
    }
  }, [existingAccounts?.accounts, setSelectedAccountId]);

  const combobox = useCombobox({
    onDropdownClose: () => combobox.resetSelectedOption(),
  });
  const options =
    existingAccounts?.accounts.map((item) => (
      <Combobox.Option value={item.id} key={item.id}>
        {item.name}
      </Combobox.Option>
    )) ?? [];
  return (
    <Stack>
      <Group>
        <Combobox
          store={combobox}
          onOptionSubmit={(val) => {
            setSelectedAccountId(val);
            combobox.closeDropdown();
          }}
        >
          <Combobox.Target>
            <InputBase
              component="button"
              type="button"
              pointer
              rightSection={<Combobox.Chevron />}
              rightSectionPointerEvents="none"
              onClick={() => combobox.toggleDropdown()}
            >
              {existingAccounts?.accounts.findLast((v) => v.id === selectedAccountId)?.name || (
                <Input.Placeholder>Select account</Input.Placeholder>
              )}
            </InputBase>
          </Combobox.Target>

          <Combobox.Dropdown>
            <Combobox.Options>{options}</Combobox.Options>
          </Combobox.Dropdown>
        </Combobox>
        {accountBalance && (
          <Group c={isBalanceLoading ? 'grey' : undefined}>
            <Text>Balance:</Text>
            <NumberFormatter prefix="$ " value={accountBalance.toFixed(2)} thousandSeparator />
          </Group>
        )}
      </Group>
      <Group>
        <SegmentedControl
          onChange={(v) => setSide(v as Side)}
          value={side}
          color={side === 'Long' ? 'green' : 'red'}
          data={['Long', 'Short']}
        />
      </Group>
    </Stack>
  );
};
