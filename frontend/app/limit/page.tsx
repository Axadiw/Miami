'use client';

import LimitPage from '@/app/limit/limitPage';
import { SharedPositionContextProvider } from '@/contexts/SharedPositionContext/SharedPositionContext';
import { LimitPositionContextProvider } from '@/app/limit/contexts/LimitPositionContext/LimitPositionContext';

export default () => (
  <SharedPositionContextProvider>
    <LimitPositionContextProvider>
      <LimitPage />
    </LimitPositionContextProvider>
  </SharedPositionContextProvider>
);
