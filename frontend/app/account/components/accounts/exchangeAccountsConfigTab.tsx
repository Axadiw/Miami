'use client';

import {
  Button,
  Card,
  Combobox,
  Group,
  Input,
  InputBase,
  Space,
  Stack,
  Text,
  TextInput,
  useCombobox,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { useAccountPageContext } from '@/contexts/AccountPageContext/AccountPageContext';
import ByBit3CommasNewAccountForm from './exchangeSpecificForms/byBit3CommasNewAccountForm';

export type ExchangeType = {
  id: string;
  name: string;
  specificForm: () => JSX.Element;
};

const exchanges: ExchangeType[] = [
  {
    id: 'bybit_3commas',
    name: 'Bybit (via 3Commas)',
    specificForm: ByBit3CommasNewAccountForm,
  },
];

export default function ExchangeAccountsConfigTab() {
  const form = useForm({
    initialValues: {
      newAccountExchangeType: '',
      newAccountName: '',
    },
    validate: {
      newAccountExchangeType: (val) => (val.length === 0 ? 'Type not selected' : null),
      newAccountName: (val) => (val.length === 0 ? 'Name not specified' : null),
    },
  });

  const { accountDetails } = useAccountPageContext();

  const combobox = useCombobox({
    onDropdownClose: () => combobox.resetSelectedOption(),
  });

  const existingAccounts = [
    { id: '1', name: 'Account 1' },
    { id: '2', name: 'Account 2' },
    { id: '3', name: 'Account 3' },
  ];

  const options = exchanges.map((item) => (
    <Combobox.Option value={item.id} key={item.id}>
      {item.name}
    </Combobox.Option>
  ));

  return (
    <>
      <Space h="md" />
      <Group align="top">
        <Card w="60%" padding="lg" radius="md" withBorder>
          <Stack>
            <form
              onSubmit={form.onSubmit(async () => {
                // eslint-disable-next-line no-console

                console.log({ ...form.values, accountDetails });
              })}
            >
              <Stack>
                <Combobox
                  store={combobox}
                  onOptionSubmit={(val) => {
                    form.setFieldValue('newAccountExchangeType', val);
                    form.setFieldValue('newAccountData', '');
                    // TODO: reset all details forms data
                    combobox.closeDropdown();
                  }}
                >
                  <Combobox.Target>
                    <InputBase
                      required
                      label="Select exchange"
                      component="button"
                      type="button"
                      pointer
                      rightSection={<Combobox.Chevron />}
                      rightSectionPointerEvents="none"
                      onClick={() => combobox.toggleDropdown()}
                    >
                      {exchanges.findLast((v) => v.id === form.values.newAccountExchangeType)
                        ?.name || <Input.Placeholder>Pick exchange</Input.Placeholder>}
                    </InputBase>
                  </Combobox.Target>

                  <Combobox.Dropdown>
                    <Combobox.Options>{options}</Combobox.Options>
                  </Combobox.Dropdown>
                </Combobox>
                <TextInput
                  required
                  label="Account friendly name"
                  value={form.values.newAccountName}
                  onChange={(event) =>
                    form.setFieldValue('newAccountName', event.currentTarget.value)
                  }
                  radius="md"
                />
                {exchanges.map((v) => (
                  <Group
                    display={v.id === form.values.newAccountExchangeType ? 'inline' : 'none'}
                    key={v.id}
                  >
                    {v.specificForm()}
                  </Group>
                ))}
              </Stack>

              <Group justify="space-between" mt="xl">
                <Button
                  type="submit"
                  radius="xl"
                  disabled={!form.isValid() || accountDetails.length === 0}
                >
                  Add new
                </Button>
              </Group>
            </form>
          </Stack>
        </Card>
        <Card w="20%" padding="lg" radius="md" withBorder>
          <Stack>
            <Text size="sm">Existing accounts:</Text>
            {existingAccounts.map((e) => (
              <Group key={e.id}>
                <Text>{e.name}</Text>
                <Button
                  onClick={() => {
                    // eslint-disable-next-line no-console
                    console.log('Removing account', e.id);
                  }}
                  variant="filled"
                  color="red"
                >
                  Delete
                </Button>
              </Group>
            ))}
          </Stack>
        </Card>
      </Group>
    </>
  );
}
