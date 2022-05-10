import React from 'react';
import type { NextPage } from 'next';
import {
  Box,
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  Heading,
} from '@fidesui/react';

import NavBar from '../../features/common/NavBar';

// import UserManagementTable from '../features/user-management/UserManagementTable';
// import UserManagementTableActions from '../../features/user-management/UserManagementTableActions';
import NewUserForm from '../../features/user-management/NewUserForm';

import { assignToken } from '../../features/user/user.slice';
import { getSession } from 'next-auth/react';
import { wrapper } from '../../app/store';

const CreateNewUser: NextPage<{ session: { username: string } }> = ({
  session,
}) => (
  <div>
    <NavBar />
    <main>
      <Box px={9} py={10}>
        <Heading mb={8} fontSize="2xl" fontWeight="semibold">
          User Management
          <Breadcrumb fontWeight="medium" fontSize="sm">
            <BreadcrumbItem>
              <BreadcrumbLink href="/user-management">
                User Management
              </BreadcrumbLink>
            </BreadcrumbItem>

            <BreadcrumbItem>
              <BreadcrumbLink href="#">Add New User</BreadcrumbLink>
            </BreadcrumbItem>
          </Breadcrumb>
        </Heading>
        <NewUserForm />
      </Box>
    </main>
  </div>
);

export default CreateNewUser;

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
