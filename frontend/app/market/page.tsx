'use client';

import MarketPage from '@/app/market/marketPage';
import { MarketPageContextProvider } from '@/contexts/MarketPageContext/MarketPageContext';

export default () => (
  <MarketPageContextProvider>
    <MarketPage />
  </MarketPageContextProvider>
);
