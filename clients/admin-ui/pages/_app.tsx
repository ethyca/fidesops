import type { AppProps } from 'next/app';
import { SessionProvider } from 'next-auth/react';
import { FidesProvider } from '@fidesui/react';

import theme from '../theme';

import '@fontsource/inter/700.css';
import '@fontsource/inter/500.css';
import '@fontsource/inter/400.css';
import '../styles/globals.css';

const MyApp = ({ Component, pageProps }: AppProps) => (
  <SessionProvider>
    <FidesProvider theme={theme}>
      <Component {...pageProps} />
    </FidesProvider>
  </SessionProvider>
);

export default MyApp;
