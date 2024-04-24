'use client';

import { SharedPositionContextProvider } from '@/contexts/SharedPositionContext/SharedPositionContext';
import { ScaledPositionContextProvider } from '@/app/scaled/contexts/ScaledPositionContext/ScaledPositionContext';
import ScaledPage from '@/app/scaled/scaledPage';

export default () => (
  <SharedPositionContextProvider>
    <ScaledPositionContextProvider>
      <ScaledPage />
    </ScaledPositionContextProvider>
  </SharedPositionContextProvider>
);
