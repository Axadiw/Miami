'use client';

import { Alert, Button, Group, Skeleton, Stack, TextInput } from '@mantine/core';
import { IconInfoCircle } from '@tabler/icons-react';
import { useEffect } from 'react';
import { useForm } from '@mantine/form';
import { useDataLayerContext } from '@/contexts/DataLayerContext';

export interface UserConfig {
  threeCommasAccountId: string;
  threeCommasApiKey: string;
  threeCommasSecret: string;
  byBitApiKey: string;
  byBitApiSecret: string;
  email: string;
}

export default function AccountPage() {
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

  const dataLayer = useDataLayerContext();
  const {
    data: fetchData,
    isLoading: fetchLoading,
    error: fetchError,
  } = dataLayer.useGetAccountInfo;
  const { error: saveError, mutate: saveAccountInfo } = dataLayer.useSaveAccountInfo;

  useEffect(() => {
    form.setValues({ ...fetchData });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fetchData]);

  const errorMessage = fetchError?.message ?? saveError?.message;

  if (fetchLoading) {
    return (
      <>
        <Skeleton height={50} circle mb="xl" />
        <Skeleton height={8} radius="xl" />
        <Skeleton height={8} mt={6} radius="xl" />
        <Skeleton height={8} mt={6} width="70%" radius="xl" />
      </>
    );
  }

  return (
    <Stack>
      {errorMessage !== undefined && (
        <Alert variant="light" color="red" radius="md" title="Error" icon={<IconInfoCircle />}>
          {errorMessage}
        </Alert>
      )}
      <form
        onSubmit={form.onSubmit(async () => {
          saveAccountInfo({ ...form.values } as UserConfig);
        })}
      >
        <Stack>
          <TextInput
            label="Email"
            value={form.values.email}
            onChange={(event) => form.setFieldValue('email', event.currentTarget.value)}
            disabled
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
