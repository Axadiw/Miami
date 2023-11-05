import React, { Suspense, useEffect } from 'react';
import { LoggedInContentContainer } from '@/components/LoggedInContentContainer/LoggedInContentContainer';
import { Authentication } from '@/components/AuthenticationForm/Authentication';
import { useLoginContext } from '@/contexts/LoginContext';
import Loading from '@/app/loading';
import { useDataLayerContext } from '@/contexts/DataLayerContext';

export function ContentContainer({ children }: { children: any }) {
  const { loginToken, setLoginToken, setLastLogoutReason } = useLoginContext();
  const dataLayer = useDataLayerContext();
  const { data: isLoginTokenValid, isSuccess: isLoginTokenValidSuccess } =
    dataLayer.useCheckIfLoginTokenIsValid();

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

  return (
    <Suspense fallback={<Loading />}>
      {isLoggedIn ? (
        <LoggedInContentContainer>{children}</LoggedInContentContainer>
      ) : (
        <Authentication />
      )}
    </Suspense>
  );
}
