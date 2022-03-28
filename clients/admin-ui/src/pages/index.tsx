import React from 'react';
import type { NextPage } from 'next';
import Head from 'next/head';
import { getSession } from 'next-auth/react';
import {
  Flex,
  Heading,
  Text,
  Button,
  Select,
  Box,
  Input,
  InputGroup,
  InputLeftElement,
  InputLeftAddon,
  Switch,
  Stack,
} from '@fidesui/react';
import { wrapper } from '../app/store';

import Header from '../features/common/Header';

import {
  ArrowDownLineIcon,
  DownloadSolidIcon,
  CloseSolidIcon,
  SearchLineIcon,
} from '../features/common/Icon';

import RequestTable from '../features/subject-requests/RequestTable';
import PIIToggle from '../features/subject-requests/PIIToggle';

import { useGetAllSubjectRequestsQuery } from '../features/subject-requests/subject-requests.slice';
import { assignToken } from '../features/user/user.slice';

const Home: NextPage = () => {
  const { data } = useGetAllSubjectRequestsQuery(null);
  return (
    <div>
      <Head>
        <title>Fides Admin UI</title>
        <meta name="description" content="Generated from FidesUI template" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />

      <main>
        <Flex
          borderBottom="1px"
          borderTop="1px"
          px={9}
          py={1}
          borderColor="gray.100"
        >
          <Button variant="ghost" mr={4} colorScheme="complimentary">
            Subject Requests
          </Button>
          <Button variant="ghost" mr={4}>
            Datastore Connections
          </Button>
          <Button variant="ghost" mr={4}>
            User Management
          </Button>
          <Button variant="ghost" rightIcon={<ArrowDownLineIcon />}>
            More
          </Button>
        </Flex>
        <Box px={9} py={10}>
          <Heading mb={8} fontSize="2xl" fontWeight="semibold">
            Subject Requests
          </Heading>
          <Stack direction="row" spacing={4} mb={6}>
            <Select placeholder="Status" size="sm" minWidth="144px">
              <option>Error</option>
              <option>Denied</option>
              <option>In Progress</option>
              <option>New</option>
              <option>Completed</option>
            </Select>
            <InputGroup size="sm">
              <InputLeftElement pointerEvents="none">
                <SearchLineIcon color="gray.300" />
              </InputLeftElement>
              <Input
                type="text"
                minWidth={200}
                placeholder="Search"
                size="sm"
              />
            </InputGroup>
            <InputGroup size="sm">
              <InputLeftAddon>From</InputLeftAddon>
              <Input type="date" />
            </InputGroup>
            <InputGroup size="sm">
              <InputLeftAddon>To</InputLeftAddon>
              <Input type="date" />
            </InputGroup>
            <Flex flexShrink={0} alignItems="center">
              <Text fontSize="xs" mr={2} size="sm">
                Reveal PII
              </Text>
              <PIIToggle />
            </Flex>
            <Button
              variant="ghost"
              flexShrink={0}
              rightIcon={<DownloadSolidIcon />}
              size="sm"
            >
              Download
            </Button>
            <Button
              variant="ghost"
              flexShrink={0}
              rightIcon={<CloseSolidIcon />}
              size="sm"
            >
              Clear all filters
            </Button>
          </Stack>
          <RequestTable requests={data && data.items} />
          <Flex justifyContent="space-between" mt={6}>
            <Text fontSize="xs" color="gray.600">
              {data ? data.items.length : 0} results
            </Text>
            <div>
              <Button disabled mr={2} size="sm">
                Previous
              </Button>
              <Button disabled size="sm">
                Next
              </Button>
            </div>
          </Flex>
        </Box>
      </main>
    </div>
  );
};

export const getServerSideProps = wrapper.getServerSideProps(
  (store) => async (context) => {
    const session = await getSession(context);
    if (session && typeof session.accessToken !== 'undefined') {
      await store.dispatch(assignToken(session.accessToken));
      console.log('Dispatched token assignment', session.accessToken);
    }
    return { props: {} };
  }
);

export default Home;
