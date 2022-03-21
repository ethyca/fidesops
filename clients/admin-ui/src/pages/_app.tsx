import type { AppProps } from 'next/app';
import { SessionProvider } from 'next-auth/react';
import { FidesProvider } from '@fidesui/react';
import { Provider as ReduxProvider } from 'react-redux';

import theme from '../theme';
import { store } from '../app/store';

import '@fontsource/inter/700.css';
import '@fontsource/inter/500.css';
import '@fontsource/inter/400.css';

if (process.env.NEXT_PUBLIC_MOCK_API) {
  // eslint-disable-next-line global-require
  require('../mocks');
}

const MyApp = ({ Component, pageProps }: AppProps) => (
  <ReduxProvider store={store}>
    <SessionProvider>
      <FidesProvider theme={theme}>
        <Component {...pageProps} />
      </FidesProvider>
    </SessionProvider>
  </ReduxProvider>
);

export default MyApp;
