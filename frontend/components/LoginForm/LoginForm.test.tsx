import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MantineProvider } from '@mantine/core';
import { LoginForm } from '@/components/LoginForm/LoginForm';

describe('LoginForm', () => {
  const setup = () => {
    const queryClient = new QueryClient();
    render(
      <MantineProvider>
        <QueryClientProvider client={queryClient}>
          <LoginForm />
        </QueryClientProvider>
      </MantineProvider>
    );
  };
  it('shows correct text', () => {
    setup();
    expect(
      screen.getByRole('button', {
        name: /login/i,
      })
    ).toBeInTheDocument();
  });
});
