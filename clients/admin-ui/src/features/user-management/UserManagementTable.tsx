import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Table, Thead, Tbody, Tr, Th } from '@fidesui/react';

import UserManagementRow from './UserManagementRow';

import { selectUserFilters, useGetAllUsersQuery } from '../user/user.slice';

const useUsersTable = () => {
  const dispatch = useDispatch();
  const filters = useSelector(selectUserFilters);

  // const handlePreviousPage = () => {
  //   dispatch(setPage(filters.page - 1));
  // };

  // const handleNextPage = () => {
  //   dispatch(setPage(filters.page + 1));
  // };

  console.log(useGetAllUsersQuery(filters));
  const { data, isLoading } = useGetAllUsersQuery(filters);
  const { items: users, total } = data || { users: [], total: 0 };

  return {
    ...filters,
    isLoading,
    users,
    // handleNextPage,
    // handlePreviousPage,
  };
};

const UserManagementTable: React.FC = () => {
  const {
    users,
    // page, size, handleNextPage, handlePreviousPage
  } = useUsersTable();
  // const startingItem = (page - 1) * size + 1;
  // const endingItem = Math.min(total, page * size);

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
