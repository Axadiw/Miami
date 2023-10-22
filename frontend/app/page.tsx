'use client';
import { useEffect, useState } from 'react';
import { Code, Group } from '@mantine/core';
import { IconBolt, IconLogout, IconScale, IconTarget } from '@tabler/icons-react';
import { MantineLogo } from '@mantine/ds';
import classes from './NavbarSimple.module.css';
import { ColorSchemeToggle } from '@/app/components/ColorSchemeToggle/ColorSchemeToggle';
import { getVersion } from '@/app/api/System';

const data = [
  { link: '', label: 'Market', icon: IconBolt },
  { link: '', label: 'Scaled', icon: IconScale },
  { link: '', label: 'Limit', icon: IconTarget },
];

export default function NavbarSimple() {
  const [active, setActive] = useState('Billing');
  const [appVersion, setAppVersion] = useState('');

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
        event.preventDefault();
        setActive(item.label);
      }}
    >
      <item.icon className={classes.linkIcon} stroke={1.5} />
      <span>{item.label}</span>
    </a>
  ));

  return (
    <nav className={classes.navbar}>
      <div className={classes.navbarMain}>
        <Group className={classes.header} justify="space-between">
          <MantineLogo size={28} />
          <Code fw={700}>{appVersion}</Code>
        </Group>
        {links}
      </div>

      <div className={classes.footer}>
        <a href="#" className={classes.link} onClick={(event) => event.preventDefault()}>
          <IconLogout className={classes.linkIcon} stroke={1.5} />
          <span>Logout</span>
        </a>
      </div>
      <ColorSchemeToggle />
    </nav>
  );
}
