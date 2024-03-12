'use client';

import {
  Alert,
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
import { IconInfoCircle } from '@tabler/icons-react';
import { useAccountPageContext } from '@/contexts/AccountPageContext/AccountPageContext';
import ByBit3CommasNewAccountForm from './exchangeSpecificForms/byBit3CommasNewAccountForm';
import { useAddNewExchangeAccount } from '@/api/useAddNewExchangeAccount';
import { useRemoveExchangeAccount } from '@/api/useRemoveExchangeAccount';
import { useListExchangeAccounts } from '@/api/useListExchangeAccounts';

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

  const {
    mutate: addNewAccount,
    error: addNewAccountError,
    isSuccess: addNewAccountIsSuccess,
  } = useAddNewExchangeAccount();
  const { mutate: removeAccount, error: removeAccountError } = useRemoveExchangeAccount();
  const { data: existingAccounts, error: listAccountError } = useListExchangeAccounts();

  const { accountDetails, setAccountDetails } = useAccountPageContext();

  const combobox = useCombobox({
    onDropdownClose: () => combobox.resetSelectedOption(),
  });

  const options = exchanges.map((item) => (
    <Combobox.Option value={item.id} key={item.id}>
      {item.name}
    </Combobox.Option>
  ));

  return (
    <>
      <Space h="md" />
      {(addNewAccountError || removeAccountError || listAccountError) && (
        <>
          <Alert variant="light" color="red" radius="md" title="Error" icon={<IconInfoCircle />}>
            {addNewAccountError?.message ??
              removeAccountError?.message ??
              listAccountError?.message}
          </Alert>
          <Space h="md" />
        </>
      )}
      {addNewAccountIsSuccess && (
        <>
          <Alert
            variant="light"
            color="greeb"
            radius="md"
            title="Added account"
            icon={<IconInfoCircle />}
          >
            Success
          </Alert>
          <Space h="md" />
        </>
      )}
      <Group align="top">
        <Card w="60%" padding="lg" radius="md" withBorder>
          <Stack>
            <form
              onSubmit={form.onSubmit(async () => {
                addNewAccount({ ...form.values, newAccountExchangeDetails: accountDetails });
                form.setFieldValue('newAccountExchangeType', '');
                form.setFieldValue('newAccountName', '');
                setAccountDetails('');
              })}
            >
              <Stack>
                <Combobox
                  store={combobox}
                  onOptionSubmit={(val) => {
                    form.setFieldValue('newAccountExchangeType', val);
                    form.setFieldValue('newAccountData', '');
                    setAccountDetails('');
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
            {existingAccounts?.accounts.map((e) => (
              <Group key={e.id}>
                <Text>{e.name}</Text>
                <Button
                  onClick={async () => {
                    removeAccount({ accountId: e.id });
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
