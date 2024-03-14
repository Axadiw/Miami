'use client';

import '@mantine/core/styles.css';
import React from 'react';
import Script from 'next/script';
import { ColorSchemeScript } from '@mantine/core';
import { RootContainer } from '@/components/RootContainer/RootContainer';

export default function RootLayout({ children }: { children: any }) {
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
          <RootContainer>{children}</RootContainer>
        </>
      </body>
    </html>
  );
}
