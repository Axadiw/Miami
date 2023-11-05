import { useForm } from '@mantine/form';
import { Alert, Button, Group, PasswordInput, Stack, TextInput } from '@mantine/core';
import { IconInfoCircle } from '@tabler/icons-react';
import { useDataLayerContext } from '@/contexts/DataLayerContext';

interface RegisterFormProps {
  switchToLoginCallback: () => void;
}

export function RegisterForm(props: RegisterFormProps) {
  const dataLayer = useDataLayerContext();
  const { error: registerError, mutateAsync: registerUser, isPending } = dataLayer.useRegisterUser;
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

  return (
    <form
      onSubmit={form.onSubmit(async () => {
        await registerUser({
          login: form.values.login,
          password: form.values.password,
          email: form.values.email,
        });
        props.switchToLoginCallback();
      })}
    >
      <Stack>
        {registerError && (
          <Alert
            variant="light"
            color="red"
            radius="md"
            title="Login error"
            icon={<IconInfoCircle />}
          >
            {registerError.message}
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
        <TextInput
          required
          label="Email"
          placeholder="user@miamitrade.pro"
          value={form.values.email}
          onChange={(event) => form.setFieldValue('email', event.currentTarget.value)}
          error={form.errors.email && 'Invalid email'}
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
          Register
        </Button>
      </Group>
    </form>
  );
}
