import React from 'react';
import type { NextPage } from 'next';
import { Box, Breadcrumb, BreadcrumbItem, BreadcrumbLink, Heading } from '@fidesui/react';

import NavBar from '../../features/common/NavBar';

// import UserManagementTable from '../features/user-management/UserManagementTable';
// import UserManagementTableActions from '../../features/user-management/UserManagementTableActions';
import NewUserForm from '../../features/user-management/NewUserForm';

const CreateNewUser: NextPage<{ session: { username: string } }> = ({ session }) => (
  <div>
    <NavBar />
    <main>
      {/* BREADCRUMBS */}
      <Box px={9} py={10}>
        <NewUserForm />
      </Box>
    </main>
  </div>
);

export default CreateNewUser;
