import React from 'react';
import { useSelector } from 'react-redux';
import type { NextPage } from 'next';
import Head from 'next/head';
import {
  Box,
  Heading,
  Text,
  Divider,
  Flex,
  Stack,
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
} from '@fidesui/react';
import { getSession } from 'next-auth/react';

import { wrapper } from '../../app/store';
import { assignToken, setUser } from '../../features/user/user.slice';
import {
  selectPrivacyRequestFilters,
  privacyRequestApi,
  setRequestId,
  useGetAllPrivacyRequestsQuery,
} from '../../features/privacy-requests/privacy-requests.slice';
import NavBar from '../../features/common/NavBar';
import RequestStatusBadge from '../../features/common/RequestStatusBadge';
import PIIToggle from '../../features/common/PIIToggle';
import PII from '../../features/common/PII';
import Clipboard from '../../features/common/Icon/Clipboard';
import ClipboardButton from '../../features/common/ClipboardButton';

const SubjectRequestDetails: NextPage<{}> = () => {
  const filters = useSelector(selectPrivacyRequestFilters);
  const { data } = useGetAllPrivacyRequestsQuery(filters);

  if (data?.items.length === 0) {
    return (
      <div>
        <Head>
          <title>Fides Admin UI - Subject Request Details</title>
          <meta name='description' content='Subject Request Details' />
          <link rel='icon' href='/favicon.ico' />
        </Head>

        <NavBar />

        <main>
          <Box px={9} py={10}>
            <Heading fontSize='2xl' fontWeight='semibold'>
              Subject Request Details
            </Heading>
            <Text>404 no subject request found</Text>
          </Box>
        </main>
      </div>
    );
  }

  const subjectRequest = data?.items[0]!;
  return (
    <div>
      <Head>
        <title>Fides Admin UI - Subject Request Details</title>
        <meta name='description' content='Subject Request Details' />
        <link rel='icon' href='/favicon.ico' />
      </Head>

      <NavBar />

      <main>
        <Box px={9} py={10}>
          <Heading fontSize='2xl' fontWeight='semibold'>
            Subject Request
            <Box mt={2} mb={9}>
              <Breadcrumb fontWeight='medium' fontSize='sm'>
                <BreadcrumbItem>
                  <BreadcrumbLink href='/'>Subject Request</BreadcrumbLink>
                </BreadcrumbItem>

                <BreadcrumbItem>
                  <BreadcrumbLink href='#'>View Details</BreadcrumbLink>
                </BreadcrumbItem>
              </Breadcrumb>
            </Box>
          </Heading>
          <Heading fontSize='lg' fontWeight='semibold' mb={4}>
            Request Details
          </Heading>
          <Divider />
          <Flex alignItems='center'>
            <Text
              mt={4}
              mb={4}
              mr={2}
              fontSize='sm'
              color='gray.900'
              fontWeight='500'
            >
              Request ID:
            </Text>
            <Text color='gray.600' fontWeight='500' fontSize='sm'>
              {subjectRequest.id}
            </Text>
            <Clipboard ml={1} />
            <ClipboardButton />
          </Flex>
          <Flex alignItems='flex-start'>
            <Text mb={4} mr={2} fontSize='sm' color='gray.900' fontWeight='500'>
              Status:
            </Text>
            <RequestStatusBadge status={subjectRequest.status} />
          </Flex>
          {/* <Text>Request Type: {subjectRequest.type}</Text> the type field doesn't exist yet */}

          <Stack direction='row'>
            <Heading fontSize='lg' fontWeight='semibold' mb={4}>
              Subject indentities
            </Heading>
            <Flex flexShrink={0} alignItems='flex-start'>
              <PIIToggle />
              <Text fontSize='xs' ml={2} size='sm'>
                Reveal PII
              </Text>
            </Flex>
          </Stack>
          <Divider />

          <Flex alignItems='center'>
            <Text
              mt={4}
              mb={4}
              mr={2}
              fontSize='sm'
              color='gray.900'
              fontWeight='500'
            >
              Email:
            </Text>
            <Text color='gray.600' fontWeight='500' fontSize='sm'>
              <PII
                data={
                  subjectRequest.identity.email
                    ? subjectRequest.identity.email
                    : ''
                }
              />
            </Text>
          </Flex>
          <Flex alignItems='flex-start'>
            <Text mb={4} mr={2} fontSize='sm' color='gray.900' fontWeight='500'>
              Mobile:
            </Text>
            <Text color='gray.600' fontWeight='500' fontSize='sm'>
              <PII
                data={
                  subjectRequest.identity.phone_number
                    ? subjectRequest.identity.phone_number
                    : ''
                }
              />
            </Text>
          </Flex>
          <Heading fontSize='lg' fontWeight='semibold' mb={4}>
            Events and logs
          </Heading>
          <Divider />
        </Box>
      </main>
    </div>
  );
};

export default SubjectRequestDetails;

export const getServerSideProps = wrapper.getServerSideProps(
  (store) => async (context) => {
    const session = await getSession(context);
    if (session && typeof session.accessToken !== 'undefined') {
      await store.dispatch(assignToken(session.accessToken));
      await store.dispatch(setUser(session.user));
      await store.dispatch(setRequestId(context.query.id as string));
      const state = store.getState();

      if (context.query.id) {
        const filters = selectPrivacyRequestFilters(state);
        delete filters.status;
        store.dispatch(
          privacyRequestApi.endpoints.getAllPrivacyRequests.initiate(filters)
        );
        await Promise.all(privacyRequestApi.util.getRunningOperationPromises());
      }

      return { props: {} };
    }

    return {
      redirect: {
        destination: '/login',
        permanent: false,
      },
    };
  }
);
