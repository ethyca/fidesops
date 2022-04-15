import React from 'react';
import NextLink from 'next/link';
import {
  Button,
  Input,
  InputGroup,
  InputLeftElement,
  Stack,
} from '@fidesui/react';

import {
  SearchLineIcon,
} from '../common/Icon';

// const useUserManagementTableActions = () => {
//   return {
   
//   };
// }

const UserManagementTableActions: React.FC = () => {
  // const {
  // } = useUserManagementTableActions();

  return (
    <Stack direction="row" spacing={4} mb={6}>
      <InputGroup size="sm">
        <InputLeftElement pointerEvents="none">
          <SearchLineIcon color="gray.300" w="17px" h="17px" />
        </InputLeftElement>
        <Input
          type="search"
          minWidth={200}
          placeholder="Search by Name or Username"
          size="sm"
          borderRadius="md"
          // value={id}
          name="search"
          // onChange={handleSearch}
        />
      </InputGroup>
      <NextLink href="/user-management/new" passHref>
        <Button
          variant="solid"
          bg="primary.800"
          color="white"
          flexShrink={0}
          size="sm"
        >
          Add New User
        </Button>
      </NextLink>
    </Stack>
  );
};

export default UserManagementTableActions;
