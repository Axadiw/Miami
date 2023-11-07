import { render, screen } from '@testing-library/react';
import React from 'react';
import DashboardPage from '@/app/dashboard/dashboardPage';
import { MockedTestContainer } from '@/test-utils/MockedTestContainer';

jest.mock('next/navigation', () => ({
  useRouter() {
    return {};
  },
  usePathname() {
    return {};
  },
}));

describe('dashboardPage', () => {
  const setup = () => {
    render(
      <MockedTestContainer initialLoginToken="dummy token">
        <DashboardPage />
      </MockedTestContainer>
    );
  };
  it('should render', () => {
    setup();
    expect(
      screen.getByText('Welcome to Miami Trade - risk aware trading platform')
    ).toBeInTheDocument();
  });
});
