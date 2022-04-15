import React from 'react';
import type { NextPage } from 'next';
import Head from 'next/head';
import { Box, Breadcrumb, BreadcrumbItem, BreadcrumbLink, Heading } from '@fidesui/react';

import NavBar from '../../features/common/NavBar';

import { getSession } from 'next-auth/react';
import { wrapper } from '../../app/store';
import { assignToken } from '../../features/user/user.slice';

// import UserManagementTable from '../features/user-management/UserManagementTable';
// import UserManagementTableActions from '../../features/user-management/UserManagementTableActions';
import NewUserForm from '../../features/user-management/NewUserForm';

const CreateNewUser: NextPage<{ session: { username: string } }> = ({ session }) => (
  <div>
    <NavBar session={session} />
    <main>
      {/* BREADCRUMBS */}
      <Box px={9} py={10}>
        <NewUserForm />
      </Box>
    </main>
  </div>
);

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

export default CreateNewUser;
