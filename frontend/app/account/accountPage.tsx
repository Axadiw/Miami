'use client';

import { rem, Tabs } from '@mantine/core';
import { IconAccessPoint, IconMessageCircle, IconPhoto } from '@tabler/icons-react';
import UserConfigTab from '@/app/account/components/userConfig/userConfigTab';
import { ChangePasswordTab } from '@/app/account/components/changePassword/changePasswordTab';
import ExchangeAccountsConfigTab from '@/app/account/components/accounts/exchangeAccountsConfigTab';

export default function AccountPage() {
  const iconStyle = { width: rem(12), height: rem(12) };
  return (
    <Tabs defaultValue="accounts">
      <Tabs.List>
        <Tabs.Tab value="accounts" leftSection={<IconAccessPoint style={iconStyle} />}>
          Accounts
        </Tabs.Tab>
        <Tabs.Tab value="options" leftSection={<IconPhoto style={iconStyle} />}>
          Options
        </Tabs.Tab>
        <Tabs.Tab value="password" leftSection={<IconMessageCircle style={iconStyle} />}>
          Change password
        </Tabs.Tab>
      </Tabs.List>

      <Tabs.Panel value="accounts">
        <ExchangeAccountsConfigTab />
      </Tabs.Panel>

      <Tabs.Panel value="options">
        <UserConfigTab />
      </Tabs.Panel>

      <Tabs.Panel value="password">
        <ChangePasswordTab />
      </Tabs.Panel>
    </Tabs>
  );
}
