import { useForm } from '@mantine/form';
import { Alert, Button, Group, PasswordInput, Stack, TextInput } from '@mantine/core';
import { IconInfoCircle } from '@tabler/icons-react';
import { useLoginUser } from '@/api/useLoginUser';

export function LoginForm() {
  const { error: loginError, mutate: loginUser } = useLoginUser();

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
        loginUser({ login: form.values.login, password: form.values.password });
      })}
    >
      <Stack>
        {loginError && (
          <Alert
            variant="light"
            color="red"
            radius="md"
            title="Login error"
            icon={<IconInfoCircle />}
          >
            {loginError.message}
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
