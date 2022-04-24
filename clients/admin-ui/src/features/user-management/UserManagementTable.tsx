import React, { useEffect, useRef, useState } from 'react';
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
} from '@fidesui/react';

import UserManagementRow from './UserManagementRow';

const UserManagementTable: React.FC = () => {
  return (
    <>
      <Table size="sm">
        <Thead>
          <Tr>
            <Th pl={0}>Name</Th>
          </Tr>
        </Thead>
        <Tbody>
          {/* Blocked until GET users is implemented */}
          {/* {users.map((user) => (
            <UserManagementRow user={user} key={user.id} />
          ))} */}
          <UserManagementRow />
        </Tbody>
      </Table>
    </>
  );
};

export default UserManagementTable;
