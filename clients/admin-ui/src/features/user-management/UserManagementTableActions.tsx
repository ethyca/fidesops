import React from 'react';
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

const UserManagementTableActions: React.FC = () => {
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
      <Button
        variant="solid"
        bg="primary.800"
        color="white"
        flexShrink={0}
        size="sm"
        // onClick={handleNewUserClick}
      >
        Add New User
      </Button>
    </Stack>
  );
};

export default UserManagementTableActions;
