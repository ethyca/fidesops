import React from 'react';
import {
  Table,
  Text,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Button,
  Flex,
} from '@fidesui/react';
import { format } from 'date-fns-tz';
import { useSelector } from 'react-redux';

import { MoreIcon } from '../common/Icon';
import RequestBadge from './RequestBadge';

import { PrivacyRequest } from './types';
import { useObscurePII } from './helpers';
import {
  selectRequestStatus,
  useGetAllPrivacyRequestsQuery,
} from './privacy-requests.slice';

interface RequestTableProps {
  requests?: PrivacyRequest[];
}

const PII: React.FC<{ data: string }> = ({ data }) => (
  <>{useObscurePII(data)}</>
);

const RequestTable: React.FC<RequestTableProps> = () => {
  const status = useSelector(selectRequestStatus);
  const { data: requests = [] } = useGetAllPrivacyRequestsQuery({ status });

  return (
    <>
      <Table size="sm">
        <Thead>
          <Tr>
            <Th pl={0}>Status</Th>
            <Th>Policy Name</Th>
            <Th>Subject Identity</Th>
            <Th>Time Received</Th>
            <Th>Reviewed By</Th>
            <Th>Request ID</Th>
            <Th />
          </Tr>
        </Thead>
        <Tbody>
          {requests.map((request) => (
            <Tr key={request.id}>
              <Td pl={0} py={0.5}>
                <RequestBadge status={request.status} />
              </Td>
              <Td py={0.5}>{}</Td>
              <Td py={0.5}>
                <Text fontSize="xs">
                  <PII
                    data={
                      request.identity
                        ? request.identity.email || request.identity.phone || ''
                        : ''
                    }
                  />
                </Text>
              </Td>
              <Td py={0.5}>
                <Text fontSize="xs">
                  {format(
                    new Date(request.created_at),
                    'MMMM d, Y, KK:mm:ss z'
                  )}
                </Text>
              </Td>
              <Td py={0.5}>
                <Text fontSize="xs">
                  <PII data={request.reviewed_by || ''} />
                </Text>
              </Td>
              <Td py={0.5}>
                <Text isTruncated fontSize="xs" maxWidth="87px">
                  {request.id}
                </Text>
              </Td>
              <Td pr={0} py={0.5} textAlign="end">
                <Button variant="ghost" size="sm">
                  <MoreIcon color="gray.700" w={18} h={18} />
                </Button>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
      <Flex justifyContent="space-between" mt={6}>
        <Text fontSize="xs" color="gray.600">
          {requests ? requests.length : 0} results
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
    </>
  );
};

RequestTable.defaultProps = {
  requests: [],
};

export default RequestTable;
