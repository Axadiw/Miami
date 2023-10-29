import { AppShell, Center, Code, Flex, Group } from '@mantine/core';
import Image from 'next/image';
import logoImage from '@/public/logo.png';
import classes from '@/app/styles/NavbarSimple.module.css';
import {
  IconBolt,
  IconDashboard,
  IconLogout,
  IconScale,
  IconSettings,
  IconTarget,
} from '@tabler/icons-react';
import { ColorSchemeToggle } from '@/components/ColorSchemeToggle/ColorSchemeToggle';
import React, { useEffect, useState } from 'react';
import { useDisclosure } from '@mantine/hooks';
import { usePathname, useRouter } from 'next/navigation';
import { useLoginContext } from '@/contexts/LoginContext';
import { useGetVersion } from '@/api/useGetVersion';

const data = [
  { link: '/', label: 'Dashboard', icon: IconDashboard },
  { link: '/market', label: 'Market', icon: IconBolt },
  { link: '/scaled', label: 'Scaled', icon: IconScale },
  { link: '/limit', label: 'Limit', icon: IconTarget },
];

export function LoggedInContentContainer({ children }: { children: any }) {
  const [active, setActive] = useState('');
  const [opened, { close: closeNavbar, toggle }] = useDisclosure();
  const { setLoginToken } = useLoginContext();

  const pathName = usePathname();
  const router = useRouter();

  const { status: versionDataFetchStatus, data: versionData } = useGetVersion();

  useEffect(() => {
    const possibleTabs = data.filter((item) => item.link === pathName);
    if (possibleTabs.length === 1) {
      setActive(possibleTabs[0].label);
    }
  }, []);

  const links = data.map((item) => (
    <a
      className={classes.link}
      data-active={item.label === active || undefined}
      href={item.link}
      key={item.label}
      onClick={(event) => {
        event.preventDefault();
        setActive(item.label);
        router.push(item.link);
        closeNavbar();
      }}
    >
      <item.icon className={classes.linkIcon} stroke={1.5} />
      <span>{item.label}</span>
    </a>
  ));

  return (
    <AppShell
      header={{ height: 48 }}
      navbar={{ width: 300, breakpoint: 'sm', collapsed: { mobile: !opened } }}
      padding="md"
    >
      <AppShell.Header>
        <Flex p={'8px'}>
          <Center>
            <Image
              src={logoImage}
              alt="logo"
              width={32}
              onClick={() => {
                toggle();
              }}
            />
          </Center>
        </Flex>
      </AppShell.Header>
      <AppShell.Navbar>
        <nav className={classes.navbar}>
          <div className={classes.navbarMain}>{links}</div>

          <div className={classes.footer}>
            <a
              href="/account"
              className={classes.link}
              onClick={(event) => {
                event.preventDefault();
                router.push('/account');
              }}
            >
              <IconSettings className={classes.linkIcon} stroke={1.5} />
              <span>Account</span>
            </a>
            <a
              href=""
              className={classes.link}
              onClick={(event) => {
                event.preventDefault();
                setLoginToken(null);
              }}
            >
              <IconLogout className={classes.linkIcon} stroke={1.5} />
              <span>Logout</span>
            </a>
            <Group p={'10px'}>
              <ColorSchemeToggle />
              <Code fw={700}>
                version: {versionDataFetchStatus === 'success' ? versionData : ''}
              </Code>
            </Group>
          </div>
        </nav>
      </AppShell.Navbar>
      <AppShell.Main>{children}</AppShell.Main>
    </AppShell>
  );
}
