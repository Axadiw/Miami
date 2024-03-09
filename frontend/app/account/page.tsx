'use client';

import AccountPage from '@/app/account/accountPage';
import { AccountPageContextProvider } from '@/contexts/AccountPageContext/AccountPageContext';

export default () => (
  <AccountPageContextProvider>
    <AccountPage />
  </AccountPageContextProvider>
);
