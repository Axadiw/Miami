'use client';

import { Stack, TextInput } from '@mantine/core';
import { useEffect, useState } from 'react';
import {
  AccountPageClearAllExchangeSpecificFormsEvent,
  useAccountPageContext,
} from '@/contexts/AccountPageContext/AccountPageContext';

export default function ByBit3CommasNewAccountForm() {
  const [accountId, setAccountId] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [apiSecret, setApiSecret] = useState('');
  const { setAccountDetails, accountPageEventEmitter } = useAccountPageContext();

  useEffect(() => {
    accountPageEventEmitter.on(AccountPageClearAllExchangeSpecificFormsEvent, () => {
      setAccountId('');
      setApiKey('');
      setApiSecret('');
    });
    return () => {
      accountPageEventEmitter.off(AccountPageClearAllExchangeSpecificFormsEvent);
    };
  }, [accountPageEventEmitter]);

  useEffect(() => {
    if (accountId && apiKey && apiSecret) {
      setAccountDetails(JSON.stringify({ accountId, apiKey, apiSecret }));
    } else {
      setAccountDetails('');
    }
  }, [accountId, apiKey, apiSecret, setAccountDetails]);

  return (
    <Stack>
      <Stack>
        <TextInput
          required
          label="3commas Account ID"
          value={accountId}
          onChange={(event) => setAccountId(event.currentTarget.value)}
          radius="md"
        />
        <TextInput
          required
          label="3commas API Key"
          value={apiKey}
          onChange={(event) => setApiKey(event.currentTarget.value)}
          radius="md"
        />
        <TextInput
          required
          label="3commas API Secret"
          value={apiSecret}
          onChange={(event) => setApiSecret(event.currentTarget.value)}
          radius="md"
        />
      </Stack>
    </Stack>
  );
}
