import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import moxios from 'moxios';
import { RootContainer } from '@/components/RootContainer/RootContainer';
import DashboardPage from '@/app/dashboard/dashboardPage';

describe('dashboardPage', () => {
  beforeEach(() => {
    // import and pass your custom axios instance to this method
    moxios.install();
  });
  afterEach(() => {
    // import and pass your custom axios instance to this method
    moxios.uninstall();
  });
  const setup = () => {
    render(
      <RootContainer>
        <DashboardPage />
      </RootContainer>
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

  it.skip('should show dashboard page after login', async () => {
    moxios.stubRequest('post', '/login', {
      status: 200,
      responseText: 'hello',
    });
    // const allowedHeaders = ['ClientName', 'ClientVersion', 'Content-Type', 'Authorization'];
    // const nockHeaders = {
    //   'Access-Control-Allow-Origin': '*',
    //   'Access-Control-Allow-Headers': allowedHeaders.join(','),
    // };
    //
    // nock(BASE_URL).intercept('*', '/login').reply(200, undefined, nockHeaders).persist();
    // const scope = nock(BASE_URL).persist().post('/login').reply(200, 'BLABLA');
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
