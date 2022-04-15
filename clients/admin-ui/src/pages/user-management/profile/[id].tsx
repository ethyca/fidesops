import React from 'react';
import type { NextPage } from 'next';
import { Box, Breadcrumb, BreadcrumbItem, BreadcrumbLink, Heading } from '@fidesui/react';

import NavBar from '../../../features/common/NavBar';

// import UserForm from '../../features/user-management/UserForm';

const Profile: NextPage<{ session: { username: string } }> = ({ session }) => (
  <div>
    <NavBar />
    <main>
      {/* BREADCRUMBS */}
      <Box px={9} py={10}>
        {/* <UserForm /> */}
        Profile page to view and edit user info
      </Box>
    </main>
  </div>
);

export default Profile;
