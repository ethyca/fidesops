import React from 'react';
import { Table, Text, Thead, Tbody, Tr, Th, Td, Button } from '@fidesui/react';
import { format } from 'date-fns-tz';

import { MoreIcon } from '../common/Icon';
import RequestBadge from './RequestBadge';
import { SubjectRequest } from './types';

import { useObscurePII } from './helpers';

interface RequestTableProps {
  requests?: SubjectRequest[];
}

const PII: React.FC<{ data: string }> = ({ data }) => (
  <>{useObscurePII(data)}</>
);

const RequestTable: React.FC<RequestTableProps> = ({ requests }) => {
  if (!requests || !requests.length) {
    return null;
  }

  return (
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
                {format(new Date(request.created_at), 'MMMM d, Y, KK:mm:ss z')}
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
  );
};

RequestTable.defaultProps = {
  requests: [],
};

export default RequestTable;
