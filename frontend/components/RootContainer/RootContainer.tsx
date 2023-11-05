import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import React from 'react';
import { MantineProvider } from '@mantine/core';
import { LoginContextProvider } from '@/contexts/LoginContext';
import { ContentContainer } from '@/components/ContentContainer/ContentContainer';
import { DataLayerContextProvider } from '@/contexts/DataLayerContext';
import { theme } from '@/theme';

export function RootContainer({ children }: { children: any }) {
  const [queryClient] = React.useState(() => new QueryClient());
  return (
    <QueryClientProvider client={queryClient}>
      <MantineProvider theme={theme}>
        <LoginContextProvider>
          <DataLayerContextProvider>
            <ContentContainer>{children}</ContentContainer>
            <ReactQueryDevtools initialIsOpen={false} />
          </DataLayerContextProvider>
        </LoginContextProvider>
      </MantineProvider>
    </QueryClientProvider>
  );
}
