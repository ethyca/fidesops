import React from 'react';
import type { NextPage } from 'next';
import { Box, Breadcrumb, BreadcrumbItem, BreadcrumbLink, Heading } from '@fidesui/react';

import NavBar from '../../features/common/NavBar';

// import UserManagementTable from '../features/user-management/UserManagementTable';
// import UserManagementTableActions from '../../features/user-management/UserManagementTableActions';
import UserForm from '../../features/user-management/UserForm';

const CreateNewUser: NextPage<{ session: { username: string } }> = ({ session }) => (
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
            <BreadcrumbLink href='#'>Add New User</BreadcrumbLink>
          </BreadcrumbItem>
        </Breadcrumb>
        </Heading>
        <UserForm />
      </Box>
    </main>
  </div>
);

export default CreateNewUser;
