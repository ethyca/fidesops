import React, { useEffect, useState } from 'react';
import type { NextPage } from 'next';
import Head from 'next/head';
import { Box, Heading } from '@fidesui/react';
import { getSession } from 'next-auth/react';
import { useRouter } from 'next/router';
import { wrapper } from '../../app/store';
import { assignToken } from '../../features/user/user.slice';

import NavBar from '../../features/common/NavBar';

import UserManagementTable from '../../features/user-management/UserManagementTable';
import UserManagementTableActions from '../../features/user-management/UserManagementTableActions';

const UserManagement: NextPage<{ session: { username: string } }> = ({
  session,
}) => {
  return (
    <div>
      <Head>
        <title>Fides Admin UI - User Management</title>
        <meta name="description" content="Generated from FidesUI template" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <NavBar />

      <main>
        <Box px={9} py={10}>
          <Heading mb={8} fontSize="2xl" fontWeight="semibold">
            User Management
          </Heading>
          <UserManagementTableActions />
          <UserManagementTable />
        </Box>
      </main>
    </div>
  );
};

export default UserManagement;

export const getServerSideProps = wrapper.getServerSideProps(
  (store) => async (context) => {
    const session = await getSession(context);
    if (session && typeof session.accessToken !== 'undefined') {
      await store.dispatch(assignToken(session.accessToken));
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
