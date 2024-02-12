import { AppShell, Center, Code, Flex, Group, useMantineColorScheme } from '@mantine/core';
import Image from 'next/image';
import {
  IconBolt,
  IconDashboard,
  IconLogout,
  IconScale,
  IconSettings,
  IconTarget,
} from '@tabler/icons-react';
import React, { useEffect, useState } from 'react';
import { useDisclosure } from '@mantine/hooks';
import { usePathname, useRouter } from 'next/navigation';
import classes from '@/app/styles/NavbarSimple.module.css';
import '@mantine/spotlight/styles.css';
import darkLogoImage from '@/public/logo-dark.png';
import lightLogoImage from '@/public/logo-light.png';
import { useLoginContext } from '@/contexts/LoginContext/LoginContext';
import { ColorSchemeToggle } from '@/components/ColorSchemeToggle/ColorSchemeToggle';
import { useDataLayerContext } from '@/contexts/DataLayerContext/DataLayerContext';

const data = [
  { link: '/', label: 'Dashboard', icon: IconDashboard },
  { link: '/market', label: 'Market', icon: IconBolt },
  { link: '/scaled', label: 'Scaled', icon: IconScale },
  { link: '/limit', label: 'Limit', icon: IconTarget },
  { link: '/account', label: 'Account', icon: IconSettings },
];

export function LoggedInContentContainer({ children }: { children: any }) {
  const [active, setActive] = useState('');
  const [opened, { close: closeNavbar, toggle }] = useDisclosure();
  const { setLoginToken } = useLoginContext();

  const pathName = usePathname();
  const router = useRouter();
  const { colorScheme } = useMantineColorScheme();
  const isDarkTheme = colorScheme === 'dark';

  const dataLayer = useDataLayerContext();
  const { status: versionDataFetchStatus, data: versionData } = dataLayer.useAppGetVersion();

  useEffect(() => {
    const possibleTabs = data.filter((item) => item.link === pathName);
    if (possibleTabs.length === 1) {
      setActive(possibleTabs[0].label);
    }
  }, [pathName]);

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
      navbar={{ width: 130, breakpoint: 'sm', collapsed: { mobile: !opened } }}
      padding="md"
    >
      <AppShell.Header>
        <Flex p="8px">
          <Center>
            <Image
              src={isDarkTheme ? darkLogoImage : lightLogoImage}
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
              href=""
              className={classes.link}
              onClick={(event) => {
                event.preventDefault();
                setLoginToken(null);
                closeNavbar();
              }}
            >
              <IconLogout className={classes.linkIcon} stroke={1.5} />
              <span>Logout</span>
            </a>
            <Group p="10px">
              <ColorSchemeToggle />
              <Code fw={700}>{versionDataFetchStatus === 'success' ? versionData : ''}</Code>
            </Group>
          </div>
        </nav>
      </AppShell.Navbar>
      <AppShell.Main>{children}</AppShell.Main>
    </AppShell>
  );
}
