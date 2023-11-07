import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MantineProvider } from '@mantine/core';
import { undefined } from 'zod';
import { DataLayer, DataLayerContext } from '@/contexts/DataLayerContext/DataLayerContext';
import { LoginContextProvider } from '@/contexts/LoginContext/LoginContext';
import { theme } from '@/theme';
import { ContentContainer } from '@/components/ContentContainer/ContentContainer';
import { MockedDataLayerBuilder } from '@/contexts/DataLayerContext/__testing__/MockedDataLayer';
import { LOGIN_TOKEN_LOCAL_STORAGE_KEY } from '@/app/consts';

export const MockedTestContainer = ({
  children,
  initialLoginToken,
  dataLayer = new MockedDataLayerBuilder()
    .loginUserReturn()
    .checkIfLoginTokenIsValidReturns()
    .appGetVersionReturns()
    .build(),
}: {
  children: any;
  initialLoginToken?: string | undefined;
  dataLayer?: DataLayer;
}) => {
  if (initialLoginToken) {
    localStorage.setItem(LOGIN_TOKEN_LOCAL_STORAGE_KEY, initialLoginToken);
  }
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: Infinity,
      },
    },
  });
  return (
    <QueryClientProvider client={queryClient}>
      <LoginContextProvider>
        <DataLayerContext.Provider value={dataLayer}>
          <MantineProvider theme={theme}>
            <ContentContainer>{children}</ContentContainer>
          </MantineProvider>
        </DataLayerContext.Provider>
      </LoginContextProvider>
    </QueryClientProvider>
  );
};
