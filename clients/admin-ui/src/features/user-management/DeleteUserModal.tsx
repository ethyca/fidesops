import React, { useState } from 'react';
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
  const [usernameValue, setUsernameValue] = useState('');
  const [confirmValue, setConfirmValue] = useState('');
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [deleteUser, deleteUserResult] = useDeleteUserMutation();

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.name === 'username') {
      setUsernameValue(event.target.value);
    } else {
      setConfirmValue(event.target.value);
    }
  };

  const deletionValidation =
    user.id &&
    confirmValue &&
    usernameValue &&
    user.username === usernameValue &&
    user.username === confirmValue
      ? true
      : false;

  const handleDeleteUser = () => {
    if (deletionValidation && user.id) {
      deleteUser(user.id);
      onClose();
    } else {
      console.log('Cant delete');
      // throw error/alert ?
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
              <Input
                isInvalid={!deletionValidation}
                name="username"
                onChange={handleChange}
                placeholder="Enter username"
                value={usernameValue}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Confirm Username</FormLabel>
              <Input
                isInvalid={!deletionValidation}
                name="confirmUsername"
                onChange={handleChange}
                placeholder="Confirm username"
                value={confirmValue}
              />
            </FormControl>
          </ModalBody>

          <ModalFooter>
            <Button onClick={onClose}>Cancel</Button>
            <Button
              disabled={!deletionValidation}
              onClick={handleDeleteUser}
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
