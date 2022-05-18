import React from 'react';
import {useSelector} from 'react-redux';
import type { NextPage } from 'next';
import Head from 'next/head';
import { Box, Heading, Text, Divider, Flex, Stack } from '@fidesui/react';
import { getSession } from 'next-auth/react';

import { wrapper } from '../../app/store';
import {assignToken, setUser} from '../../features/user/user.slice';
import {
    selectPrivacyRequestFilters,
    privacyRequestApi,
    setRequestId,
    useGetAllPrivacyRequestsQuery
} from '../../features/privacy-requests/privacy-requests.slice';
import NavBar from '../../features/common/NavBar';
import RequestStatusBadge from '../../features/common/RequestStatusBadge'
import PIIToggle from '../../features/common/PIIToggle'
import PII from "../../features/common/PII";


const SubjectRequestDetails: NextPage<{}> = () => {


    const filters = useSelector(selectPrivacyRequestFilters);
    const {data} = useGetAllPrivacyRequestsQuery(filters);


    if (data?.items.length === 0){
        return (
            <div>
                <Head>
                    <title>Fides Admin UI - Subject Request Details</title>
                    <meta name="description" content="Subject Request Details" />
                    <link rel="icon" href="/favicon.ico" />
                </Head>

                <NavBar />

                <main>
                    <Box px={9} py={10}>
                        <Heading fontSize="2xl" fontWeight="semibold">
                            Subject Request Details
                        </Heading>
                        <Text>404 no subject request  found</Text>
                    </Box>
                </main>
            </div>
        );
    }

   const subjectRequest = data?.items[0]!
    return (
        <div>
            <Head>
                <title>Fides Admin UI - Subject Request Details</title>
                <meta name="description" content="Subject Request Details" />
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <NavBar />

            <main>
                <Box px={9} py={10}>
                    <Heading fontSize="2xl" fontWeight="semibold">
                        Subject Request Details
                    </Heading>
                    <Divider/>
                    <Text>Request ID: {subjectRequest.id}</Text>
                    <Text>Status: <RequestStatusBadge status={subjectRequest.status}/></Text>
                    {/* <Text>Request Type: {subjectRequest.type}</Text> the type field doesn't exist yet */}

                    <Stack direction='row'>
                        <Heading fontSize="2xl" fontWeight="semibold">
                            Subject indentities
                        </Heading>
                        <Flex flexShrink={0} alignItems="center">
                            <Text fontSize="xs" mr={2} size="sm">
                                Reveal PII
                            </Text>
                            <PIIToggle />
                        </Flex>
                    </Stack>
                    <Divider/>
                    <Text> Email: <PII data={subjectRequest.identity.email?subjectRequest.identity.email: '' }/></Text>
                    <Text> Mobile: <PII data={subjectRequest.identity.phone_number?subjectRequest.identity.phone_number: '' }/></Text>
                    <Heading fontSize="2xl" fontWeight="semibold">
                        Events and logs
                    </Heading>
                    <Divider/>

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
            await store.dispatch(setRequestId(context.query.id as string))
            const state = store.getState()

            if(context.query.id){
                const filters = selectPrivacyRequestFilters(state)
                delete filters.status
                store.dispatch(
                    privacyRequestApi.endpoints.getAllPrivacyRequests.initiate(filters)
                )
                await Promise.all(privacyRequestApi.util.getRunningOperationPromises());
            }



            return { props: { } };
        }

        return {
            redirect: {
                destination: '/login',
                permanent: false,
            },
        };
    }
);
