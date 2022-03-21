import { Table, Thead, Tbody, Tr, Th, Td, Button } from '@fidesui/react';

import { MoreIcon } from '../Icon';
import RequestBadge from './RequestBadge';

const RequestTable = () => (
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
      <Tr>
        <Td pl={0} py={0.5}>
          <RequestBadge status="error" />
        </Td>
        <Td py={0.5}>james.braithwaite@email.com</Td>
        <Td py={0.5}>August 4, 2021, 09:35:46 PST</Td>
        <Td py={0.5}>Sammie_Shanahan@gmail.com</Td>
        <Td pr={0} py={0.5} textAlign="end">
          <Button variant="ghost" size="sm">
            <MoreIcon color="gray.700" w={18} h={18} />
          </Button>
        </Td>
      </Tr>
      <Tr>
        <Td pl={0} py={0.5}>
          <RequestBadge status="denied" />
        </Td>
        <Td py={0.5}>555-325-685-126</Td>
        <Td py={0.5}>August 4, 2021, 09:35:46 PST</Td>
        <Td py={0.5}>Richmond33@yahoo.com</Td>
        <Td pr={0} py={0.5} textAlign="end">
          <Button variant="ghost" size="sm">
            <MoreIcon color="gray.700" w={18} h={18} />
          </Button>
        </Td>
      </Tr>
    </Tbody>
  </Table>
);

export default RequestTable;
