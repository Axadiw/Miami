import { useToggle } from '@mantine/hooks';
import { Anchor, Group, Paper, PaperProps, Space } from '@mantine/core';
import React from 'react';
import { RegisterForm } from '@/components/RegisterForm/RegisterForm';
import { LoginForm } from '@/components/LoginForm/LoginForm';
import { ColorSchemeToggle } from '@/components/ColorSchemeToggle/ColorSchemeToggle';

export function Authentication(props: PaperProps) {
  const [type, toggle] = useToggle(['login', 'register']);

  return (
    <Paper radius="md" p="xl" withBorder {...props}>
      {type === 'register' ? (
        <RegisterForm
          switchToLoginCallback={() => {
            toggle();
          }}
        />
      ) : (
        <LoginForm />
      )}
      <Group justify="space-between" mt="xl">
        <Anchor component="button" type="button" c="dimmed" onClick={() => toggle()} size="xs">
          {type === 'register'
            ? 'Already have an account? Login'
            : "Don't have an account? Register"}
        </Anchor>
      </Group>
      <Space h="lg" />
      <ColorSchemeToggle />
    </Paper>
  );
}
