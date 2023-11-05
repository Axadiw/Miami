import { render, screen } from '@testing-library/react';
import { LoginForm } from '@/components/LoginForm/LoginForm';
import { RootContainer } from '@/components/RootContainer/RootContainer';

describe('LoginForm', () => {
  const setup = () => {
    render(
      <RootContainer>
        <LoginForm />
      </RootContainer>
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
