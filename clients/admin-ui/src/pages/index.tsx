import { Box, Heading } from '@fidesui/react';
import type { NextPage } from 'next';
import Head from 'next/head';
import { getSession } from 'next-auth/react';
import { wrapper } from '../app/store';
import { assignToken, setUser } from '../features/user/user.slice';
import { User } from '../features/user/types';

import NavBar from '../features/common/NavBar';

import RequestTable from '../features/privacy-requests/RequestTable';
import RequestFilters from '../features/privacy-requests/RequestFilters';

const Home: NextPage<{ session: { user: User } }> = ({ session }) => {
  return (
    <div>
      <Head>
        <title>Fides Admin UI</title>
        <meta name='description' content='Generated from FidesUI template' />
        <link rel='icon' href='/favicon.ico' />
      </Head>

      <NavBar />

      <main>
        <Box px={9} py={10}>
          <Heading mb={8} fontSize='2xl' fontWeight='semibold'>
            Subject Requests
          </Heading>
          <RequestFilters />
          <RequestTable />
        </Box>
      </main>
    </div>
  );
};

export const getServerSideProps = wrapper.getServerSideProps(
  (store) => async (context) => {
    const session = await getSession(context);

    if (session && typeof session.accessToken !== 'undefined') {
      await store.dispatch(assignToken(session.accessToken));
      await store.dispatch(setUser(session.user));
      return { props: { session } };
    }

    return {
      redirect: {
        destination: '/login',
        permanent: false,
      },
    };
  }
);

export default Home;
