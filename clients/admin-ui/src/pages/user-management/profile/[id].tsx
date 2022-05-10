import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import type { NextPage } from 'next';
import {
  Box,
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  Heading,
} from '@fidesui/react';
import { useRouter } from 'next/router';
import NavBar from '../../../features/common/NavBar';
import EditUserForm from '../../../features/user-management/EditUserForm';
import {
  useGetUserByIdQuery,
  userApi,
  assignToken,
  setManagedUser,
} from '../../../features/user/user.slice';

import { wrapper } from '../../../app/store';
import { getSession } from 'next-auth/react';

const Profile: NextPage = () => {
  return (
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
                <BreadcrumbLink href="#">Edit User</BreadcrumbLink>
              </BreadcrumbItem>
            </Breadcrumb>
          </Heading>
          <EditUserForm />
        </Box>
      </main>
    </div>
  );
};

export default Profile;

export const getServerSideProps = wrapper.getServerSideProps(
  (store) => async (context) => {
    const session = await getSession(context);
    if (session && typeof session.accessToken !== 'undefined') {
      await store.dispatch(assignToken(session.accessToken));
      console.log('Found ID on this page', context.query.id);

      if (context.query.id) {
        store.dispatch(
          userApi.endpoints.getUserById.initiate(context.query.id)
        );
        store.dispatch(
          userApi.endpoints.getUserPermissions.initiate(context.query.id)
        );
        await Promise.all(userApi.util.getRunningOperationPromises());
      }
      return { props: { session, query: context.query } };
    }

    return {
      redirect: {
        destination: '/login',
        permanent: false,
      },
    };
  }
);
