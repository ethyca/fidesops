import React, { useState } from 'react';
import {
  Text,
  Tr,
  Td,
  Button,
  ButtonGroup,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Portal,
} from '@fidesui/react';

import { MoreIcon } from '../common/Icon';
import DeleteUserModal from './DeleteUserModal';
import { User } from '../user/types';
// import Router from 'next/router';

interface UserManagementRowProps {
  user: User;
}

const useUserManagementRow = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const handleMenuOpen = () => setMenuOpen(true);
  const handleMenuClose = () => setMenuOpen(false);

  return {
    menuOpen,
    handleMenuClose,
    handleMenuOpen,
  };
};

const UserManagementRow: React.FC<UserManagementRowProps> = ({ user }) => {
  const {
    handleMenuOpen,
    handleMenuClose,
    menuOpen,
  } = useUserManagementRow();

  // const handleEditUser = () => {
  //   Router.push(/user-management/profile/${user.id})
  // }

  const showMenu = menuOpen;

  return (
  <>
    <Tr
      // key={user.id}
      _hover={{ bg: 'gray.50' }}
      height="36px"
    >
    <Td pl={0} py={1}>
          {/* {user.name} */}
          Name
      </Td>
      <Td pr={0} py={1} textAlign="end" position="relative">
      <ButtonGroup>
          <Menu onOpen={handleMenuOpen} onClose={handleMenuClose}>
          <MenuButton
            as={Button}
            size="xs"
            bg="white"
          >
              <MoreIcon color="gray.700" w={18} h={18} />
          </MenuButton>
            <Portal>
              <MenuList shadow="xl">
                <MenuItem
                  _focus={{ color: 'complimentary.500', bg: 'gray.100' }}
                  // onClick={handleEditUser}
                >
                  <Text fontSize="sm">Edit</Text>
                </MenuItem>
                {DeleteUserModal(user)}
              </MenuList>
            </Portal>
          </Menu>
        </ButtonGroup>
        </Td>
        </Tr>
        </>
  );
};

export default UserManagementRow;
