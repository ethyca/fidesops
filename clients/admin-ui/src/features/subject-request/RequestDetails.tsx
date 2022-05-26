import { Box, Divider, Flex, Heading, Tag, Text } from '@fidesui/react';
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
        Request details
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

      <Flex alignItems='center'>
        <Text mb={4} mr={2} fontSize='sm' color='gray.900' fontWeight='500'>
          Request Type:
        </Text>
        <Tag
          color='white'
          bg='primary.400'
          fontWeight='medium'
          fontSize='sm'
          mr={1}
          mb={4}
        >
          {subjectRequest.policy.name}
        </Tag>
      </Flex>
      <Flex alignItems='flex-start'>
        <Text mb={4} mr={2} fontSize='sm' color='gray.900' fontWeight='500'>
          Status:
        </Text>
        <Box>
          <RequestStatusBadge status={status} />
        </Box>
      </Flex>
    </>
  );
};

export default RequestDetails;
