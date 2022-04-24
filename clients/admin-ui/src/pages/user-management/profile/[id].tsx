import React from 'react';
import type { NextPage } from 'next';
import { Box, Breadcrumb, BreadcrumbItem, BreadcrumbLink, Heading } from '@fidesui/react';

import NavBar from '../../../features/common/NavBar';

// import UserForm from '../../features/user-management/UserForm';

const Profile: NextPage<{ session: { username: string } }> = ({ session }) => (
  <div>
    <NavBar />
    <main>
      <Box px={9} py={10}>
      <Heading mb={8} fontSize="2xl" fontWeight="semibold">
          User Management
          <Breadcrumb fontWeight='medium' fontSize='sm'>
          <BreadcrumbItem>
            <BreadcrumbLink href='/user-management'>User Management</BreadcrumbLink>
          </BreadcrumbItem>

          <BreadcrumbItem>
            <BreadcrumbLink href='#'>Edit User</BreadcrumbLink>
          </BreadcrumbItem>
        </Breadcrumb>
        </Heading>
        Profile page to view and edit user info
      </Box>
    </main>
  </div>
);

export default Profile;
