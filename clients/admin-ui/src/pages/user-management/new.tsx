import {
  Box,
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  Heading,
} from '@fidesui/react';
import type { NextPage } from 'next';
import Link from 'next/link';
import React from 'react';

import { USER_MANAGEMENT_ROUTE } from '../../constants';
import ProtectedRoute from '../../features/auth/ProtectedRoute';
import NavBar from '../../features/common/NavBar';
import NewUserForm from '../../features/user-management/NewUserForm';

const CreateNewUser: NextPage = () => (
  <ProtectedRoute>
    <div>
      <NavBar />
      <main>
        <Box px={9} py={10}>
          <Heading fontSize='2xl' fontWeight='semibold'>
            User Management
            <Box mt={2} mb={7}>
              <Breadcrumb fontWeight='medium' fontSize='sm'>
                <BreadcrumbItem>
                  <Link href={USER_MANAGEMENT_ROUTE} passHref>
                    <BreadcrumbLink href={USER_MANAGEMENT_ROUTE}>
                      User Management
                    </BreadcrumbLink>
                  </Link>
                </BreadcrumbItem>

                <BreadcrumbItem>
                  <BreadcrumbLink href='#'>Add New User</BreadcrumbLink>
                </BreadcrumbItem>
              </Breadcrumb>
            </Box>
          </Heading>
          <NewUserForm />
        </Box>
      </main>
    </div>
  </ProtectedRoute>
);

export default CreateNewUser;
