import React, { useState } from 'react';
import {
  Button,
  FormControl,
  Input,
  MenuItem,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Stack,
  Text,
  useDisclosure,
} from '@fidesui/react';

import { User } from '../user/types';
import { useUpdatePasswordMutation } from '../user/user.slice';

function UpdatePasswordModal(user: User) {
  const [oldPasswordValue, setOldPasswordValue] = useState('');
  const [newPasswordValue, setNewPasswordValue] = useState('');
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [changePassword, changePasswordResult] = useUpdatePasswordMutation();

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
    }
  };

  return (
    <>
      <MenuItem
        _focus={{ color: 'complimentary.500', bg: 'gray.100' }}
        onClick={onOpen}
      >
        <Text fontSize="sm">Update Password</Text>
      </MenuItem>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Update Password</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <Stack direction={'column'} spacing="15px">
              <FormControl>
                <Input
                  isRequired
                  name="oldPassword"
                  onChange={handleChange}
                  placeholder="Old Password"
                  value={usernameValue}
                />
              </FormControl>
              <FormControl>
                <Input
                  isRequired
                  name="newPassword"
                  onChange={handleChange}
                  placeholder="New Password"
                  value={confirmValue}
                />
              </FormControl>
            </Stack>
          </ModalBody>

          <ModalFooter>
            <Button
              onClick={onClose}
              marginRight={'10px'}
              size={'sm'}
              variant={'solid'}
              bg="white"
              width={'50%'}
            >
              Cancel
            </Button>
            <Button
              disabled={!passwordValidation}
              onClick={handleChangePassword}
              mr={3}
              size={'sm'}
              variant="solid"
              bg="primary.800"
              color="white"
              width={'50%'}
            >
              Change Password
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}

export default UpdatePasswordModal;
