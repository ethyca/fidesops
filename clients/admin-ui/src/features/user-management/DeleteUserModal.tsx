import {
  Button,
  FormControl,
  FormLabel,
  Input,
  MenuItem,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Text,
  useDisclosure,
} from '@fidesui/react';

import { User } from '../user/types';
import { useDeleteUserMutation } from '../user/user.slice';

function DeleteUserModal(user: User) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [deleteUser, deleteUserResult] = useDeleteUserMutation();

  const handleDeleteUser = () => {
    if (user.id) {
      deleteUser(user.id);
    } else {
      console.log('Cant delete');
    }
  };

  return (
    <>
      <MenuItem
        _focus={{ color: 'complimentary.500', bg: 'gray.100' }}
        onClick={onOpen}
      >
        <Text fontSize="sm">Delete</Text>
      </MenuItem>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Delete User</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <FormControl>
              <FormLabel>Username</FormLabel>
              <Input placeholder="Enter username" />
            </FormControl>
            <FormControl>
              <FormLabel>Confirm Username</FormLabel>
              <Input placeholder="Confirm username" />
            </FormControl>
          </ModalBody>

          <ModalFooter>
            <Button onClick={onClose}>Cancel</Button>
            {/* Disable delete user button when either field is blank or the fields don't match ? */}
            <Button
              onClick={handleDeleteUser}
              // colorScheme='blue'
              mr={3}
            >
              Delete User
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}

export default DeleteUserModal;
