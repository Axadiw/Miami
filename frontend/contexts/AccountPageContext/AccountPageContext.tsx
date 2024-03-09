import {
  createContext,
  Dispatch,
  ReactNode,
  SetStateAction,
  useContext,
  useMemo,
  useState,
} from 'react';

interface AccountPageContext {
  accountDetails: string;
  setAccountDetails: Dispatch<SetStateAction<string>>;
}

export const AccountPageContext = createContext<AccountPageContext>({} as AccountPageContext);

export const useAccountPageContext = () => useContext(AccountPageContext);

export const AccountPageContextProvider = ({ children }: { children: ReactNode }) => {
  const [accountDetails, setAccountDetails] = useState<string>('');

  const value = useMemo(
    () => ({
      accountDetails,
      setAccountDetails,
    }),
    [accountDetails]
  );

  return <AccountPageContext.Provider value={value}>{children}</AccountPageContext.Provider>;
};
