import React from 'react';
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
import UserForm from '../../../features/user-management/UserForm';
import { useGetUserByIdQuery } from '../../../features/user/user.slice';

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
          <UserForm />
        </Box>
      </main>
    </div>
  );
};

export default Profile;
