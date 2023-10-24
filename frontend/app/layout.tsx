'use client';
import '@mantine/core/styles.css';
import Image from 'next/image';
import React, { useEffect, useState } from 'react';
import {
  AppShell,
  Center,
  Code,
  ColorSchemeScript,
  Flex,
  Group,
  MantineProvider,
} from '@mantine/core';
import { theme } from '@/theme';
import { getVersion } from '@/app/api/System';
import classes from '@/app/components/NavBar/NavbarSimple.module.css';
import { IconBolt, IconDashboard, IconLogout, IconScale, IconTarget } from '@tabler/icons-react';
import { useDisclosure } from '@mantine/hooks';
import logoImage from '../public/logo.png';
import { usePathname } from 'next/navigation';

const data = [
  { link: '/', label: 'Dashboard', icon: IconDashboard },
  { link: '/market', label: 'Market', icon: IconBolt },
  { link: '/scaled', label: 'Scaled', icon: IconScale },
  { link: '/limit', label: 'Limit', icon: IconTarget },
];

export default function RootLayout({ children }: { children: any }) {
  const [active, setActive] = useState('');
  const [appVersion, setAppVersion] = useState('');
  const [opened, { toggle }] = useDisclosure();

  const pathName = usePathname();

  useEffect(() => {
    const possibleTabs = data.filter((item) => item.link === pathName);
    if (possibleTabs.length === 1) {
      setActive(possibleTabs[0].label);
    }
  }, []);

  useEffect(() => {
    const updateVersion = async () => {
      setAppVersion((await getVersion()) ?? '');
    };
    updateVersion();
  }, []);

  const links = data.map((item) => (
    <a
      className={classes.link}
      data-active={item.label === active || undefined}
      href={item.link}
      key={item.label}
      onClick={(event) => {
        setActive(item.label);
      }}
    >
      <item.icon className={classes.linkIcon} stroke={1.5} />
      <span>{item.label}</span>
    </a>
  ));

  return (
    <html lang="en">
      <head>
        <ColorSchemeScript />
        <link rel="shortcut icon" href="/favicon.svg" />
        <meta
          name="viewport"
          content="minimum-scale=1, initial-scale=1, width=device-width, user-scalable=no"
        />
      </head>
      <body>
        <MantineProvider theme={theme}>
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
                  <a href={classes.link} className={classes.link}>
                    <IconLogout className={classes.linkIcon} stroke={1.5} />
                    <span>Logout</span>
                  </a>
                  <Group>
                    <Code fw={700}>version: {appVersion}</Code>
                  </Group>
                </div>
              </nav>
            </AppShell.Navbar>

            <AppShell.Main>{children}</AppShell.Main>
          </AppShell>
        </MantineProvider>
      </body>
    </html>
  );
}
