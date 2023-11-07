'use client';

import { rem, Tabs } from '@mantine/core';
import { IconMessageCircle, IconPhoto } from '@tabler/icons-react';
import UserConfigTab from '@/app/account/components/userConfig/userConfigTab';
import { ChangePasswordTab } from '@/app/account/components/changePassword/changePasswordTab';

export default function AccountPage() {
  const iconStyle = { width: rem(12), height: rem(12) };
  return (
    <Tabs defaultValue="options">
      <Tabs.List>
        <Tabs.Tab value="options" leftSection={<IconPhoto style={iconStyle} />}>
          Options
        </Tabs.Tab>
        <Tabs.Tab value="password" leftSection={<IconMessageCircle style={iconStyle} />}>
          Change password
        </Tabs.Tab>
      </Tabs.List>

      <Tabs.Panel value="options">
        <UserConfigTab />
      </Tabs.Panel>

      <Tabs.Panel value="password">
        <ChangePasswordTab />
      </Tabs.Panel>
    </Tabs>
  );
}
