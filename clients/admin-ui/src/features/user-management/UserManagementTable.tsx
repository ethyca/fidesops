import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Table, Thead, Tbody, Tr, Th } from '@fidesui/react';

import UserManagementRow from './UserManagementRow';

import { selectUserFilters, useGetAllUsersQuery } from '../user/user.slice';
import { User } from '../user/types';

interface UsersTableProps {
  users?: User[];
}

const useUsersTable = () => {
  const dispatch = useDispatch();
  const filters = useSelector(selectUserFilters);

  // const handlePreviousPage = () => {
  //   dispatch(setPage(filters.page - 1));
  // };

  // const handleNextPage = () => {
  //   dispatch(setPage(filters.page + 1));
  // };

  const { data, isLoading } = useGetAllUsersQuery(filters);
  const { items: users, total } = data || { users: [], total: 0 };

  return {
    ...filters,
    isLoading,
    users,
    total,
    // handleNextPage,
    // handlePreviousPage,
  };
};

const UserManagementTable: React.FC<UsersTableProps> = () => {
  const {
    users,
    total,
    // page, size, handleNextPage, handlePreviousPage
  } = useUsersTable();
  // const startingItem = (page - 1) * size + 1;
  // const endingItem = Math.min(total, page * size);

  return (
    <>
      <Table size="sm">
        <Thead>
          <Tr>
            <Th pl={0}>Username</Th>
          </Tr>
        </Thead>
        <Tbody>
          {users?.map((user) => (
            <UserManagementRow user={user} key={user.id} />
          ))}
        </Tbody>
      </Table>
    </>
  );
};

UserManagementTable.defaultProps = {
  users: [],
};

export default UserManagementTable;
