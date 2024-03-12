import {
  createContext,
  Dispatch,
  ReactNode,
  SetStateAction,
  useContext,
  useMemo,
  useState,
} from 'react';
import EventEmitter from 'eventemitter3';

interface AccountPageContext {
  accountDetails: string;
  setAccountDetails: Dispatch<SetStateAction<string>>;
  accountPageEventEmitter: EventEmitter<string | symbol, any>;
}

export const AccountPageContext = createContext<AccountPageContext>({} as AccountPageContext);

export const useAccountPageContext = () => useContext(AccountPageContext);

export const AccountPageClearAllExchangeSpecificFormsEvent =
  'AccountPageClearAllExchangeSpecificFormsEvent';

export const AccountPageContextProvider = ({ children }: { children: ReactNode }) => {
  const [accountDetails, setAccountDetails] = useState<string>('');
  const accountPageEventEmitter = useMemo(() => new EventEmitter(), []);

  const value = useMemo(
    () => ({
      accountDetails,
      setAccountDetails,
      accountPageEventEmitter,
    }),
    [accountDetails, accountPageEventEmitter]
  );

  return <AccountPageContext.Provider value={value}>{children}</AccountPageContext.Provider>;
};
