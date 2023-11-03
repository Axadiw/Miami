import React, { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { LoggedInContentContainer } from '@/components/LoggedInContentContainer/LoggedInContentContainer';
import { Authentication } from '@/components/AuthenticationForm/Authentication';
import { useLoginContext } from '@/contexts/LoginContext';
import Loading from '@/app/loading';
import {
  checkIfLoginTokenIsValid,
  IsLoginTokenValidCacheKey,
} from '@/api/useCheckIfLoginTokenIsValid';

export function AppContainer({ children }: { children: any }) {
  const { loginToken, setLoginToken, setLastLogoutReason } = useLoginContext();

  const { data: isLoginTokenValid, isSuccess: isLoginTokenValidSuccess } = useQuery({
    queryKey: [IsLoginTokenValidCacheKey, loginToken],
    queryFn: () => checkIfLoginTokenIsValid(loginToken),
    refetchInterval: 60 * 1000,
  });

  useEffect(() => {
    if (loginToken && !isLoginTokenValid && isLoginTokenValidSuccess) {
      setLastLogoutReason('Token expired');
      setLoginToken(null);
    }
  }, [isLoginTokenValid, isLoginTokenValidSuccess, loginToken, setLastLogoutReason, setLoginToken]);

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
