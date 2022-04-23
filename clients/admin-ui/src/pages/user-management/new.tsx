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
      {/* BREADCRUMBS */}
      <Box px={9} py={10}>
        <UserForm />
      </Box>
    </main>
  </div>
);

export default CreateNewUser;
