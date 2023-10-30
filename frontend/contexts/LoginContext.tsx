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
  loginToken: string | null;
  setLoginToken: Dispatch<SetStateAction<string | null>>;
}

export const LoginContsext = createContext<LoginContext>({} as LoginContext);

export const useLoginContext = () => useContext(LoginContext);

export const LoginContextProvider = ({ children }: { children: ReactNode }) => {
  const [loginToken, setLoginToken] = useState<string | null>(null);

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

  const value = useMemo(() => ({ loginToken, setLoginToken }), [loginToken, setLoginToken]);

  return <LoginContext.Provider value={value}>{children}</LoginContext.Provider>;
};
