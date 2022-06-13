import { Box, Heading } from '@fidesui/react';
import type { NextPage } from 'next';
import Head from 'next/head';
import React from 'react';

import ProtectedRoute from '../../features/auth/ProtectedRoute';
import NavBar from '../../features/common/NavBar';
import ConnectionFilters from '../../features/datastore-connections/ConnectionFilters';
import ConnectionGrid from '../../features/datastore-connections/ConnectionGrid';

const DatastoreConnections: NextPage = () => (
  <ProtectedRoute>
    <div>
      <Head>
        <title>Fides Admin UI - Datastore Connections</title>
        <meta name="description" content="" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <NavBar />

      <main>
        <Box px={9} py={10}>
          <Heading fontSize="2xl" fontWeight="semibold">
            Datastore Connection Management
          </Heading>
          <ConnectionFilters />
          <ConnectionGrid />
        </Box>
      </main>
    </div>
  </ProtectedRoute>
);
export default DatastoreConnections;
