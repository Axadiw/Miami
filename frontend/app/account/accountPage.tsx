'use client';

import { Alert, Button, Group, Stack, TextInput } from '@mantine/core';
import { IconInfoCircle } from '@tabler/icons-react';
import { useEffect, useState } from 'react';
import { useForm } from '@mantine/form';
import { getAccountInfo } from '@/api/GetAccountInfo';
import { saveAccountInfo } from '@/api/SaveAccountInfo';
import { useLoginContext } from '@/contexts/LoginContext';

export interface UserConfig {
  threeCommasAccountId: string;
  threeCommasApiKey: string;
  threeCommasSecret: string;
  byBitApiKey: string;
  byBitApiSecret: string;
  email: string;
}

export default function AccountPage() {
  const [error, setError] = useState<string | undefined>();
  const { loginToken } = useLoginContext();

  const form = useForm({
    initialValues: {
      threeCommasAccountId: '',
      threeCommasApiKey: '',
      threeCommasSecret: '',
      byBitApiKey: '',
      byBitApiSecret: '',
      email: '',
    },
  });

  useEffect(() => {
    const updateInfo = async () => {
      if (loginToken) {
        try {
          setError(undefined);
          const accountInfo = await getAccountInfo(loginToken);
          form.setValues({ ...accountInfo });
        } catch (error: any) {
          setError(error.message);
        }
      }
    };
    updateInfo().catch((error: any) => setError(error.message));
  }, [loginToken]);
  return (
    <Stack>
      {error !== undefined && (
        <Alert variant="light" color="red" radius="md" title="Error" icon={<IconInfoCircle />}>
          {error}
        </Alert>
      )}
      <form
        onSubmit={form.onSubmit(async () => {
          if (loginToken) {
            try {
              setError(undefined);
              await saveAccountInfo(loginToken, { ...form.values } as UserConfig);
            } catch (error: any) {
              setError(error.message);
            }
          }
        })}
      >
        <Stack>
          <TextInput
            label="Email"
            value={form.values.email}
            onChange={(event) => form.setFieldValue('email', event.currentTarget.value)}
            disabled={true}
            radius="md"
          />
          <TextInput
            label="3commas Account ID"
            value={form.values.threeCommasAccountId}
            onChange={(event) =>
              form.setFieldValue('threeCommasAccountId', event.currentTarget.value)
            }
            radius="md"
          />
          <TextInput
            label="3commas API Key"
            value={form.values.threeCommasApiKey}
            onChange={(event) => form.setFieldValue('threeCommasApiKey', event.currentTarget.value)}
            radius="md"
          />
          <TextInput
            label="3commas API Secret"
            value={form.values.threeCommasSecret}
            onChange={(event) => form.setFieldValue('threeCommasSecret', event.currentTarget.value)}
            radius="md"
          />
          <TextInput
            label="Bybit API Key"
            value={form.values.byBitApiKey}
            onChange={(event) => form.setFieldValue('byBitApiKey', event.currentTarget.value)}
            radius="md"
          />
          <TextInput
            label="Bybit API Secret"
            value={form.values.byBitApiSecret}
            onChange={(event) => form.setFieldValue('byBitApiSecret', event.currentTarget.value)}
            radius="md"
          />
        </Stack>

        <Group justify="space-between" mt="xl">
          <Button type="submit" radius="xl">
            Save
          </Button>
        </Group>
      </form>
    </Stack>
  );
}
