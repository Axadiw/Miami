import { useForm } from '@mantine/form';
import { Alert, Button, Group, PasswordInput, Stack, TextInput } from '@mantine/core';
import { IconInfoCircle } from '@tabler/icons-react';
import { useLoginContext } from '@/contexts/LoginContext/LoginContext';
import { useDataLayerContext } from '@/contexts/DataLayerContext/DataLayerContext';

export function LoginForm() {
  const dataLayer = useDataLayerContext();
  const { error: loginError, mutateAsync: loginUser, isPending } = dataLayer.useLoginUser();

  const { setLoginToken, setLastLogoutReason, lastLogoutReason } = useLoginContext();

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
        setLastLogoutReason(undefined);
        const loginResponse = await loginUser({
          login: form.values.login,
          password: form.values.password,
        });
        setLoginToken(loginResponse.token);
      })}
    >
      <Stack>
        {(loginError || lastLogoutReason) && (
          <Alert
            variant="light"
            color="red"
            radius="md"
            title="Login error"
            icon={<IconInfoCircle />}
          >
            {loginError?.message ?? lastLogoutReason}
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
        <Button type="submit" radius="xl" loading={isPending}>
          Login
        </Button>
      </Group>
    </form>
  );
}
