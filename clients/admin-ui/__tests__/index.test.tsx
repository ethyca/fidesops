// __tests__/index.test.tsx
import { render, screen } from './test-utils';
import { SessionProvider } from 'next-auth/react';
import Home from '../src/pages/index';

describe('Home', () => {
  it('renders the Subject Requests page by default', () => {
    render(
      <SessionProvider>
        <Home />
      </SessionProvider>
    );

    const message = screen.getAllByText('Subject Requests')[0];
    expect(message).toBeInTheDocument();
  });
});
