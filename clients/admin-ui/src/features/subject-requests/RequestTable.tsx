import { Table, Thead, Tbody, Tr, Th, Td, Button } from '@fidesui/react';

import { MoreIcon } from '../common/Icon';
import RequestBadge from './RequestBadge';

import { useAppSelector } from '../../app/hooks';
import { subjectRequests } from './subject-requests.slice';

const RequestTable = () => {
  const requests = useAppSelector(subjectRequests);
  return (
    <Table size="sm">
      <Thead>
        <Tr>
          <Th pl={0}>Status</Th>
          <Th>Subject Identity</Th>
          <Th>Time Received</Th>
          <Th>Reviewer</Th>
          <Th />
        </Tr>
      </Thead>
      <Tbody>
        {requests.map((request) => (
          <Tr key={request.id}>
            <Td pl={0} py={0.5}>
              <RequestBadge status={request.status} />
            </Td>
            <Td py={0.5}>{request.identity}</Td>
            <Td py={0.5}>{request.timeReceived}</Td>
            <Td py={0.5}>{request.reviewer}</Td>
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

export default RequestTable;
