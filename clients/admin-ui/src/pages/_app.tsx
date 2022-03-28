import type { AppProps } from 'next/app';
import { SessionProvider } from 'next-auth/react';
import { FidesProvider } from '@fidesui/react';

import theme from '../theme';
import { wrapper } from '../app/store';

import '@fontsource/inter/700.css';
import '@fontsource/inter/500.css';
import '@fontsource/inter/400.css';

if (process.env.NEXT_PUBLIC_MOCK_API) {
  // eslint-disable-next-line global-require
  require('../mocks');
}

const MyApp = ({ Component, pageProps }: AppProps) => (
  <SessionProvider>
    <FidesProvider theme={theme}>
      <Component {...pageProps} />
    </FidesProvider>
  </SessionProvider>
);

export default wrapper.withRedux(MyApp);
