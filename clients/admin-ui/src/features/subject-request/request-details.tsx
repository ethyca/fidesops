import { Divider, Flex, Heading, Text } from '@fidesui/react';
import React from 'react';

import ClipboardButton from '../common/ClipboardButton';
import RequestStatusBadge from '../common/RequestStatusBadge';
import { PrivacyRequest } from '../privacy-requests/types';

type RequestDetailsProps = {
  subjectRequest: PrivacyRequest;
};

const RequestDetails = ({ subjectRequest }: RequestDetailsProps) => {
  const { id, status } = subjectRequest;

  return (
    <>
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
        <Text color='gray.600' fontWeight='500' fontSize='sm' mr={1}>
          {id}
        </Text>
        <ClipboardButton requestId={id} />
      </Flex>
      <Flex alignItems='flex-start'>
        <Text mb={4} mr={2} fontSize='sm' color='gray.900' fontWeight='500'>
          Status:
        </Text>
        <RequestStatusBadge status={status} />
      </Flex>
      {/* <Text>Request Type: {subjectRequest.type}</Text> the type field doesn't exist yet */}
    </>
  );
};

export default RequestDetails;
