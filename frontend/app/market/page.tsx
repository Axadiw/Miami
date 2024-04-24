'use client';

import MarketPage from '@/app/market/marketPage';
import { SharedPositionContextProvider } from '@/contexts/SharedPositionContext/SharedPositionContext';
import { MarketPositionContextProvider } from '@/app/market/contexts/LimitPositionContext/MarketPositionContext';

export default () => (
  <SharedPositionContextProvider>
    <MarketPositionContextProvider>
      <MarketPage />
    </MarketPositionContextProvider>
  </SharedPositionContextProvider>
);
