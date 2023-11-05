import { MantineProvider } from '@mantine/core';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import React, { Suspense } from 'react';
import Loading from '@/app/loading';
import { theme } from '@/theme';
import { LoginContextProvider } from '@/contexts/LoginContext';
import { ContentContainer } from '@/components/ContentContainer/ContentContainer';
import { DataLayerContextProvider } from '@/contexts/DataLayerContext';

export function RootContainer({ children }: { children: any }) {
  const [queryClient] = React.useState(() => new QueryClient());
  return (
    <Suspense fallback={<Loading />}>
      <MantineProvider theme={theme}>
        <QueryClientProvider client={queryClient}>
          <LoginContextProvider>
            <DataLayerContextProvider>
              <ContentContainer>{children}</ContentContainer>
              <ReactQueryDevtools initialIsOpen={false} />
            </DataLayerContextProvider>
          </LoginContextProvider>
        </QueryClientProvider>
      </MantineProvider>
    </Suspense>
  );
}
