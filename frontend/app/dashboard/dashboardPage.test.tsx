import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import { MantineProvider } from '@mantine/core';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import DashboardPage from '@/app/dashboard/dashboardPage';
import { ContentContainer } from '@/components/ContentContainer/ContentContainer';
import { MockedDataLayerBuilder } from '@/contexts/__testing__/MockedDataLayer';
import { DataLayerContext } from '@/contexts/DataLayerContext';
import { theme } from '@/theme';
import { LoginContextProvider } from '@/contexts/LoginContext';

jest.mock('next/navigation', () => ({
  useRouter() {
    return {
      prefetch: () => null,
    };
  },
  usePathname() {
    return {};
  },
}));

describe('dashboardPage', () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: Infinity,
      },
    },
  });
  const dataLayer = new MockedDataLayerBuilder()
    .loginUserReturn()
    .checkIfLoginTokenIsValidReturns()
    .appGetVersionReturns()
    .build();
  const setup = () => {
    render(
      <QueryClientProvider client={queryClient}>
        <LoginContextProvider>
          <DataLayerContext.Provider value={dataLayer}>
            <MantineProvider theme={theme}>
              <ContentContainer>
                <DashboardPage />
              </ContentContainer>
            </MantineProvider>
          </DataLayerContext.Provider>
        </LoginContextProvider>
      </QueryClientProvider>
    );
  };
  it('should show login page if no login token available', () => {
    setup();
    expect(
      screen.queryByText('Welcome to Miami Trade - risk aware trading platform')
    ).not.toBeInTheDocument();
    expect(
      screen.getByRole('button', {
        name: /login/i,
      })
    ).toBeInTheDocument();
  });

  it('should show dashboard page after login', async () => {
    setup();
    fireEvent.change(
      screen.getByRole('textbox', {
        name: /login/i,
      }),
      { target: { value: 'login' } }
    );
    fireEvent.change(screen.getByLabelText(/password \*/i), { target: { value: 'password' } });
    fireEvent.click(
      screen.getByRole('button', {
        name: /login/i,
      })
    );

    await waitFor(() => {
      expect(
        screen.getByText('Welcome to Miami Trade - risk aware trading platform')
      ).toBeInTheDocument();
    });
    expect(
      screen.queryByRole('button', {
        name: /login/i,
      })
    ).not.toBeInTheDocument();
  });
});
