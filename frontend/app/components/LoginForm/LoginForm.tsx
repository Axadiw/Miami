import { useForm } from '@mantine/form';
import { Alert, Button, Group, PaperProps, PasswordInput, Stack, TextInput } from '@mantine/core';
import { loginUser } from '@/app/api/User';
import { useState } from 'react';
import { IconInfoCircle } from '@tabler/icons-react';
import { useSetLoginToken } from '@/app/hooks/useSetLoginToken';

export function LoginForm(props: PaperProps) {
  const [error, setError] = useState<string | undefined>();
  const setLoginToken = useSetLoginToken();
  const form = useForm({
    initialValues: {
      login: '',
      password: '',
    },

    validate: {
      login: (val) => (val.length <= 0 ? "Login can't be empty" : null),
      password: (val) => (val.length <= 0 ? 'Password should include at least 6 characters' : null),
    },
  });

  return (
    <form
      onSubmit={form.onSubmit(async () => {
        try {
          setError(undefined);
          setLoginToken((await loginUser(form.values.login, form.values.password)).token);
        } catch (error: any) {
          setError(error.message);
        }
      })}
    >
      <Stack>
        {error !== undefined && (
          <Alert
            variant="light"
            color="red"
            radius="md"
            title="Login error"
            icon={<IconInfoCircle />}
          >
            {error}
          </Alert>
        )}
        <TextInput
          required
          label="Login"
          placeholder="Login"
          value={form.values.login}
          onChange={(event) => form.setFieldValue('login', event.currentTarget.value)}
          radius="md"
        />
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
        <Button type="submit" radius="xl">
          Login
        </Button>
      </Group>
    </form>
  );
}
