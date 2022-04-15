import React, { useRef, useState } from 'react';
import {
  Tag,
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

const UserManagementRow: React.FC = (user) => {
  const {
    handleMenuOpen,
    handleMenuClose,
    menuOpen,
  } = useUserManagementRow();
  const showMenu = menuOpen;

  return (
  <>
    <Tr
      // key={user.id}
      _hover={{ bg: 'gray.50' }}
      height="36px"
    >
    <Td pl={0} py={1}>
        <Tag
          color="white"
          bg="primary.400"
          px={2}
          py={0.5}
          size="sm"
          fontWeight="medium"
        >
          {/* {user.name} */}
          Name
        </Tag>
      </Td>
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
                  // onClick={handleViewUser}
                  // redirects to specific profile/[id] page
                >
                  <Text fontSize="sm">View</Text>
                </MenuItem>
                <MenuItem
                  _focus={{ color: 'complimentary.500', bg: 'gray.100' }}
                  // onClick={handleDeleteUser}
                  // deletes user at [id]
                >
                  <Text fontSize="sm">Delete</Text>
                </MenuItem>
              </MenuList>
            </Portal>
          </Menu>
        </ButtonGroup>
        </Tr>
        </>
  );
};

export default UserManagementRow;
