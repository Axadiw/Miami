'use client';

import { Alert, Button, Group, Stack, TextInput } from '@mantine/core';
import { useLoginToken } from '@/app/hooks/useLoginToken';
import { IconInfoCircle } from '@tabler/icons-react';
import { useEffect, useState } from 'react';
import { getAccountInfo, saveAccountInfo } from '@/app/api/User';
import { useForm } from '@mantine/form';

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
  const token = useLoginToken();

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
  useEffect(() => {}, []);

  useEffect(() => {
    const updateVersion = async () => {
      if (token) {
        try {
          setError(undefined);
          const accountInfo = await getAccountInfo(token);
          form.setValues({ ...accountInfo });
        } catch (error: any) {
          setError(error.message);
        }
      }
    };
    updateVersion();
  }, [token]);
  return (
    <Stack>
      {error !== undefined && (
        <Alert variant="light" color="red" radius="md" title="Error" icon={<IconInfoCircle />}>
          {error}
        </Alert>
      )}
      <form
        onSubmit={form.onSubmit(async () => {
          if (token) {
            try {
              setError(undefined);
              await saveAccountInfo(token, { ...form.values } as UserConfig);
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
