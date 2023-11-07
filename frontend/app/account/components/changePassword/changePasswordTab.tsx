import { useForm } from '@mantine/form';
import { Alert, Button, Group, PasswordInput, Stack } from '@mantine/core';
import { IconInfoCircle } from '@tabler/icons-react';
import { useDataLayerContext } from '@/contexts/DataLayerContext/DataLayerContext';

export function ChangePasswordTab() {
  const dataLayer = useDataLayerContext();
  const {
    error: changePasswordError,
    mutateAsync: changePassword,
    isPending,
    isSuccess,
  } = dataLayer.useChangePassword();

  const form = useForm({
    initialValues: {
      oldPassword: '',
      newPassword: '',
      newPasswordConfirm: '',
    },

    validate: {
      newPasswordConfirm: (val, values) =>
        val !== values.newPassword ? "Password don't match" : null,
    },
  });

  return (
    <form
      onSubmit={form.onSubmit(async () => {
        await changePassword({
          oldPassword: form.values.oldPassword,
          newPassword: form.values.newPassword,
        });
      })}
    >
      <Stack>
        {changePasswordError && (
          <Alert
            variant="light"
            color="red"
            radius="md"
            title="Login error"
            icon={<IconInfoCircle />}
          >
            {changePasswordError.message}
          </Alert>
        )}
        {isSuccess && (
          <Alert
            variant="light"
            color="green"
            radius="md"
            title="Change password"
            icon={<IconInfoCircle />}
          >
            Success
          </Alert>
        )}

        <PasswordInput
          required
          label="Current Password"
          value={form.values.oldPassword}
          onChange={(event) => form.setFieldValue('oldPassword', event.currentTarget.value)}
          radius="md"
        />
        <PasswordInput
          required
          label="New Password"
          value={form.values.newPassword}
          onChange={(event) => form.setFieldValue('newPassword', event.currentTarget.value)}
          radius="md"
        />
        <PasswordInput
          required
          label="Confirm new Password"
          value={form.values.newPasswordConfirm}
          onChange={(event) => form.setFieldValue('newPasswordConfirm', event.currentTarget.value)}
          error={form.errors.newPasswordConfirm}
          onBlur={() => form.validate()}
          radius="md"
        />
      </Stack>

      <Group justify="space-between" mt="xl">
        <Button type="submit" radius="xl" loading={isPending}>
          Change password
        </Button>
      </Group>
    </form>
  );
}
