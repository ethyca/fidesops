import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Flex,
  Text,
  Button,
  Select,
  Input,
  InputGroup,
  InputLeftElement,
  InputLeftAddon,
  Stack,
  useToast,
} from '@fidesui/react';

import {
  SearchLineIcon,
} from '../common/Icon';
// import { statusPropMap } from './RequestBadge';

// import { PrivacyRequestStatus } from './types';
// import {
//   setRequestStatus,
//   setRequestId,
//   setRequestFrom,
//   setRequestTo,
//   clearAllFilters,
//   selectPrivacyRequestFilters,
//   requestCSVDownload,
// } from './privacy-requests.slice';
// import { selectUserToken } from '../user/user.slice';

const useUserManagementTableActions = () => {
  const filters = useSelector(selectPrivacyRequestFilters);
  const token = useSelector(selectUserToken);
  const dispatch = useDispatch();
  const toast = useToast();
  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    dispatch(setRequestId(event.target.value));
  };

  return {
    handleSearchChange,
    ...filters,
  };
};

const UserManagementTableActions: React.FC = () => {
  const {
    handleSearchChange,
    id,
  } = useUserManagementTableActions();
  return (
    <Stack direction="row" spacing={4} mb={6}>
      <InputGroup size="sm">
        <InputLeftElement pointerEvents="none">
          <SearchLineIcon color="gray.300" w="17px" h="17px" />
        </InputLeftElement>
        <Input
          type="search"
          minWidth={200}
          placeholder="Search"
          size="sm"
          borderRadius="md"
          value={id}
          name="search"
          onChange={handleSearchChange}
        />
      </InputGroup>
      <Button
        variant="ghost"
        flexShrink={0}
        size="sm"
        onClick={handleAddNewUserClick}
      >
        Add New User
      </Button>
    </Stack>
  );
};

export default UserManagementTableActions;
