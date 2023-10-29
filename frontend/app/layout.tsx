// @ts-nocheck
'use client';
import '@mantine/core/styles.css';
import React, { Suspense } from 'react';
import { ColorSchemeScript, MantineProvider } from '@mantine/core';
import { theme } from '@/theme';
import Loading from '@/app/loading';
import { LoginContextProvider } from '@/contexts/LoginContext';
import { AppContainer } from '@/components/AppContainer/AppContainer';
import Script from 'next/script';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

export default function RootLayout({ children }: { children: any }) {
  const queryClient = new QueryClient();
  return (
    <html lang="en">
      <head>
        <ColorSchemeScript />
        <link rel="shortcut icon" href="/favicon.png" />
        <meta
          name="viewport"
          content="minimum-scale=1, initial-scale=1, width=device-width, user-scalable=no"
        />
        <title>Miami Trade</title>
      </head>
      <body>
        <>
          {process.env.NODE_ENV !== 'development' && (
            <>
              <Script src="https://www.googletagmanager.com/gtag/js?id=G-9C1V7Z121V" />
              <Script id="google-analytics">
                {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'G-9C1V7Z121V');
          `}
              </Script>
            </>
          )}
          <Suspense fallback={<Loading />}>
            <MantineProvider theme={theme}>
              <LoginContextProvider>
                <QueryClientProvider client={queryClient}>
                  <AppContainer>{children}</AppContainer>
                  <ReactQueryDevtools initialIsOpen={false} />
                </QueryClientProvider>
              </LoginContextProvider>
            </MantineProvider>
          </Suspense>
        </>
      </body>
    </html>
  );
}
