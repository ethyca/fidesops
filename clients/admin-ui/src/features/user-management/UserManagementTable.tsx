import React, { useEffect, useRef, useState } from 'react';
import {
  Table,
  Text,
  Thead,
  Tbody,
  Tr,
  Th,
  Button,
  Flex,
} from '@fidesui/react';
import { useDispatch, useSelector } from 'react-redux';

import debounce from 'lodash.debounce';

import { PrivacyRequest } from './types';
import {
  selectPrivacyRequestFilters,
  useGetAllPrivacyRequestsQuery,
  setPage,
} from './privacy-requests.slice';

import UserManagementRow from './UserManagementRow';

// const useUserManagementTable = () => {
//   const dispatch = useDispatch();

//   pagination ?
//   const filters = useSelector(selectPrivacyRequestFilters);
//   const [cachedFilters, setCachedFilters] = useState(filters);
//   const updateCachedFilters = useRef(
//     debounce((updatedFilters) => setCachedFilters(updatedFilters), 250)
//   );
//   useEffect(() => {
//     updateCachedFilters.current(filters);
//   }, [setCachedFilters, filters]);

//   const handlePreviousPage = () => {
//     dispatch(setPage(filters.page - 1));
//   };

//   const handleNextPage = () => {
//     dispatch(setPage(filters.page + 1));
//   };

//   const { data, isLoading } = useGetAllPrivacyRequestsQuery(cachedFilters);
//   const { items: requests, total } = data || { items: [], total: 0 };
//   return {
//     ...filters,
//     isLoading,
//     requests,
//     total,
//     handleNextPage,
//     handlePreviousPage,
//   };
// };

const UserManagementTable: React.FC = () => {
//   const { requests, total, page, size, handleNextPage, handlePreviousPage } =
//     useUserManagementTable();
//   const startingItem = (page - 1) * size + 1;
//   const endingItem = Math.min(total, page * size);
  return (
    <>
      <Table size="sm">
        <Thead>
          <Tr>
            <Th pl={0}>User</Th>
          </Tr>
        </Thead>
        <Tbody>
          {users.map((user) => (
            <UserManagementRow user={user} key={user.id} />
          ))}
        </Tbody>
      </Table>
      {/* <Flex justifyContent="space-between" mt={6}>
        <Text fontSize="xs" color="gray.600">
          Showing {Number.isNaN(startingItem) ? 0 : startingItem} to{' '}
          {Number.isNaN(endingItem) ? 0 : endingItem} of{' '}
          {Number.isNaN(total) ? 0 : total} results
        </Text>
        <div>
          <Button
            disabled={page <= 1}
            onClick={handlePreviousPage}
            mr={2}
            size="sm"
          >
            Previous
          </Button>
          <Button
            disabled={page * size >= total}
            onClick={handleNextPage}
            size="sm"
          >
            Next
          </Button>
        </div>
      </Flex> */}
    </>
  );
};

// RequestTable.defaultProps = {
//   requests: [],
// };

export default UserManagementTable;
