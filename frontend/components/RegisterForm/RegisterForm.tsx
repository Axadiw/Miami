import { useForm } from '@mantine/form';
import { Alert, Button, Group, PasswordInput, Stack, TextInput } from '@mantine/core';
import { useState } from 'react';
import { IconInfoCircle } from '@tabler/icons-react';
import { registerUser } from '@/api/RegisterUser';

interface RegisterFormProps {
  switchToLoginCallback: () => void;
}

export function RegisterForm(props: RegisterFormProps) {
  const [error, setError] = useState<string | undefined>();
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
        try {
          setError(undefined);
          await registerUser(form.values.login, form.values.password, form.values.email);
          props.switchToLoginCallback();
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
        <Button type="submit" radius="xl">
          Register
        </Button>
      </Group>
    </form>
  );
}
