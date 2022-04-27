import React from 'react';
import type { NextPage } from 'next';
import { Box, Breadcrumb, BreadcrumbItem, BreadcrumbLink, Heading } from '@fidesui/react';
import NavBar from '../../../features/common/NavBar';
import UserForm from '../../../features/user-management/UserForm';

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
        <UserForm 
        // existingId={id}
        existingId={"1"}
        />
      </Box>
    </main>
  </div>
);

export default Profile;

// export async function getServerSideProps(context) {
  // const { id } = context.query;
  // const res = await fetch(`https://restcountries.eu/rest/v2/name/${id}`);
    // fetch is getUserById call
  // const user = await res.json();

  // return { props: { user } };
// }
