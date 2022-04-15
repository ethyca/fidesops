import React from 'react';
import type { NextPage } from 'next';
import Head from 'next/head';
import { Box, Breadcrumb, BreadcrumbItem, BreadcrumbLink, Heading } from '@fidesui/react';

import NavBar from '../../features/common/NavBar';

// import UserManagementTable from '../features/user-management/UserManagementTable';
import UserManagementTableActions from '../../features/user-management/UserManagementTableActions';

const UserManagement: NextPage<{ session: { username: string } }> = ({ session }) => (
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
        {/* <Breadcrumb fontWeight='medium' fontSize='sm'>
          <BreadcrumbItem>
            <BreadcrumbLink href='/user-management'>User Management</BreadcrumbLink>
          </BreadcrumbItem>

          <BreadcrumbItem>
            <BreadcrumbLink href='#'></BreadcrumbLink>
          </BreadcrumbItem>

          <BreadcrumbItem isCurrentPage>
            <BreadcrumbLink href='#'></BreadcrumbLink>
          </BreadcrumbItem>
        </Breadcrumb> */}
        <UserManagementTableActions />
        {/* <UserManagementTable /> */}
      </Box>
    </main>
  </div>
);

export default UserManagement;
