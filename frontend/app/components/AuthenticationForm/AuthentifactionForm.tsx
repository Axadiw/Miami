import { upperFirst, useToggle } from '@mantine/hooks';
import { useForm } from '@mantine/form';
import {
  Anchor,
  Button,
  Group,
  Paper,
  PaperProps,
  PasswordInput,
  Stack,
  Text,
  TextInput,
} from '@mantine/core';
import { useEffect } from 'react';
import { loginUser, registerUser } from '@/app/api/User';

export function AuthenticationForm(props: PaperProps) {
  const [type, toggle] = useToggle(['login', 'register']);
  const form = useForm({
    initialValues: {
      email: '',
      login: '',
      password: '',
    },

    validate: {
      email: (val) => (/^\S+@\S+$/.test(val) ? null : 'Invalid email'),
      login: (val) => (val.length <= 0 ? "Login can't be empty" : null),
      password: (val) => (val.length <= 6 ? 'Password should include at least 6 characters' : null),
    },
  });

  useEffect(() => {}, [form.values]);

  return (
    <Paper radius="md" p="xl" withBorder {...props}>
      <Text size="lg" fw={500}>
        Welcome to Miami Trade, {type} with
      </Text>

      <form
        onSubmit={form.onSubmit(async () => {
          if (type === 'register') {
            await registerUser(form.values.login, form.values.password, form.values.email);
          } else {
            await loginUser(form.values.login, form.values.password);
          }
        })}
      >
        <Stack>
          <TextInput
            required
            label="Login"
            placeholder="Login"
            value={form.values.login}
            onChange={(event) => form.setFieldValue('login', event.currentTarget.value)}
            radius="md"
          />

          {type === 'register' && (
            <TextInput
              required
              label="Email"
              placeholder="user@miamitrade.pro"
              value={form.values.email}
              onChange={(event) => form.setFieldValue('email', event.currentTarget.value)}
              error={form.errors.email && 'Invalid email'}
              radius="md"
            />
          )}
          <PasswordInput
            required
            label="Password"
            placeholder="Your password"
            value={form.values.password}
            onChange={(event) => form.setFieldValue('password', event.currentTarget.value)}
            error={form.errors.password && 'Password should include at least 6 characters'}
            radius="md"
          />
        </Stack>

        <Group justify="space-between" mt="xl">
          <Anchor component="button" type="button" c="dimmed" onClick={() => toggle()} size="xs">
            {type === 'register'
              ? 'Already have an account? Login'
              : "Don't have an account? Register"}
          </Anchor>
          <Button type="submit" radius="xl">
            {upperFirst(type)}
          </Button>
        </Group>
      </form>
    </Paper>
  );
}
