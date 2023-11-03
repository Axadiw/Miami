import {
  createContext,
  Dispatch,
  ReactNode,
  SetStateAction,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react';
import { LOGIN_TOKEN_LOCAL_STORAGE_KEY } from '@/app/consts';

interface LoginContext {
  loginToken: string | null | undefined;
  setLoginToken: Dispatch<SetStateAction<string | null | undefined>>;
  lastLogoutReason: string | undefined;
  setLastLogoutReason: Dispatch<SetStateAction<string | undefined>>;
}

export const LoginContext = createContext<LoginContext>({} as LoginContext);

export const useLoginContext = () => useContext(LoginContext);

export const LoginContextProvider = ({ children }: { children: ReactNode }) => {
  const [loginToken, setLoginToken] = useState<string | null | undefined>(undefined);
  const [lastLogoutReason, setLastLogoutReason] = useState<string | undefined>(undefined);

  useEffect(() => {
    setLoginToken(localStorage.getItem(LOGIN_TOKEN_LOCAL_STORAGE_KEY));
  }, []);

  useEffect(() => {
    if (loginToken) {
      localStorage.setItem(LOGIN_TOKEN_LOCAL_STORAGE_KEY, loginToken);
    } else {
      localStorage.removeItem(LOGIN_TOKEN_LOCAL_STORAGE_KEY);
    }
  }, [loginToken]);

  const value = useMemo(
    () => ({ loginToken, setLoginToken, lastLogoutReason, setLastLogoutReason }),
    [lastLogoutReason, loginToken]
  );

  return <LoginContext.Provider value={value}>{children}</LoginContext.Provider>;
};
