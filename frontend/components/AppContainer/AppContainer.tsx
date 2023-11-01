import React from 'react';
import { LoggedInContentContainer } from '@/components/LoggedInContentContainer/LoggedInContentContainer';
import { Authentication } from '@/components/AuthenticationForm/Authentication';
import { useLoginContext } from '@/contexts/LoginContext';
import Loading from '@/app/loading';

export function AppContainer({ children }: { children: any }) {
  const { loginToken } = useLoginContext();

  if (loginToken === undefined) {
    return <Loading />;
  }

  const isLoggedIn = loginToken !== null;

  return isLoggedIn ? (
    <LoggedInContentContainer>{children}</LoggedInContentContainer>
  ) : (
    <Authentication />
  );
}
