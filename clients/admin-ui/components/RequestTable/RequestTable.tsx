import {
  Table,
  Thead,
  Tbody,
  Tfoot,
  Tr,
  Th,
  Td,
  TableCaption,
  Badge,
  Button,
} from '@fidesui/react';

import { More } from '../Icon';

const RequestTable = () => (
  <Table size="sm">
    <Thead>
      <Tr>
        <Th>Status</Th>
        <Th>Subject Identity</Th>
        <Th>Time Received</Th>
        <Th>Reviewer</Th>
        <Th />
      </Tr>
    </Thead>
    <Tbody>
      <Tr>
        <Td>
          <Badge bg="red.800" color="white" width={107} textAlign="center">
            Error
          </Badge>
        </Td>
        <Td>james.braithwaite@email.com</Td>
        <Td>August 4, 2021, 09:35:46 PST</Td>
        <Td>Sammie_Shanahan@gmail.com</Td>
        <Td>
          <Button variant="ghost">
            <More color="gray.700" />
          </Button>
        </Td>
      </Tr>
      <Tr>
        <Td>
          <Badge bg="red.500" color="white" width={107} textAlign="center">
            Denied
          </Badge>
        </Td>
        <Td>555-325-685-126</Td>
        <Td>August 4, 2021, 09:35:46 PST</Td>
        <Td>Richmond33@yahoo.com</Td>
        <Td>
          <Button variant="ghost">
            <More color="gray.700" />
          </Button>
        </Td>
      </Tr>
    </Tbody>
  </Table>
);

export default RequestTable;
