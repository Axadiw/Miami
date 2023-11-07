import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import DashboardPage from '@/app/dashboard/dashboardPage';
import { MockedDataLayerBuilder } from '@/contexts/DataLayerContext/__testing__/MockedDataLayer';
import { MockedTestContainer } from '@/test-utils/MockedTestContainer';

jest.mock('next/navigation', () => ({
  useRouter() {
    return {};
  },
  usePathname() {
    return {};
  },
}));

describe('ContentContainer', () => {
  describe('Login flow', () => {
    const dataLayer = new MockedDataLayerBuilder()
      .loginUserReturn()
      .checkIfLoginTokenIsValidReturns()
      .appGetVersionReturns()
      .build();

    const setup = () => {
      render(
        <MockedTestContainer dataLayer={dataLayer}>
          <DashboardPage />
        </MockedTestContainer>
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
});
