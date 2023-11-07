import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { LoginForm } from '@/components/LoginForm/LoginForm';
import { MockedTestContainer } from '@/test-utils/MockedTestContainer';
import { MockedDataLayerBuilder } from '@/contexts/DataLayerContext/__testing__/MockedDataLayer';
import { MockedMutationResultError } from '@/contexts/DataLayerContext/__testing__/MockedMutationResultError';
import { DataLayer } from '@/contexts/DataLayerContext/DataLayerContext';
import { MockedMutationResult } from '@/contexts/DataLayerContext/__testing__/MockedMutationResult';
import { LOGIN_TOKEN_LOCAL_STORAGE_KEY } from '@/app/consts';

jest.mock('next/navigation', () => ({
  useRouter() {
    return {};
  },
  usePathname() {
    return {};
  },
}));

describe('LoginForm', () => {
  const typeLoginAndPassword = (login: string, password: string) => {
    fireEvent.change(
      screen.getByRole('textbox', {
        name: /login/i,
      }),
      { target: { value: login } }
    );
    fireEvent.change(screen.getByLabelText(/password \*/i), { target: { value: password } });
    fireEvent.click(
      screen.getByRole('button', {
        name: /login/i,
      })
    );
  };
  const setup = (dataLayer?: DataLayer) => {
    render(
      <MockedTestContainer dataLayer={dataLayer}>
        <LoginForm />
      </MockedTestContainer>
    );
  };
  it('shows error for too short login', () => {
    setup();

    typeLoginAndPassword('lo', 'p');
    expect(screen.getByText('Login should have at least 3 characters')).toBeInTheDocument();
  });

  it('shows error after incorrect login', () => {
    const dataLayer = new MockedDataLayerBuilder()
      .loginUserReturn(
        MockedMutationResultError(
          {
            login: 'log',
            password: 'a',
          },
          { token: '' },
          new Error('TEST error')
        )
      )
      .checkIfLoginTokenIsValidReturns()
      .appGetVersionReturns()
      .build();
    setup(dataLayer);

    typeLoginAndPassword('log', 'a');
    expect(screen.getByText('TEST error')).toBeInTheDocument();
  });

  it('sets login token after successful login', async () => {
    const dataLayer = new MockedDataLayerBuilder()
      .loginUserReturn(
        MockedMutationResult(
          {
            login: 'log',
            password: 'a',
          },
          { token: 'newToken' }
        )
      )
      .checkIfLoginTokenIsValidReturns()
      .appGetVersionReturns()
      .build();
    setup(dataLayer);

    typeLoginAndPassword('log', 'a');

    await waitFor(() => {
      expect(localStorage.getItem(LOGIN_TOKEN_LOCAL_STORAGE_KEY)).toEqual('newToken');
    });
  });
});
