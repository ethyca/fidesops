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

function DeleteUserModal(user) {
    const { isOpen, onOpen, onClose } = useDisclosure()
    // const deleteUser(id) { 
    //   // call delete user from API and delete by id here
    // }
  
    return (
      <>
        <MenuItem
          _focus={{ color: 'complimentary.500', bg: 'gray.100' }}
          onClick={onOpen}
        >
          <Text fontSize="sm">Delete</Text>
        </MenuItem>
        <Modal
          isOpen={isOpen}
          onClose={onClose}
        >
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Delete User</ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <FormControl>
                <FormLabel>User name</FormLabel>
                <Input placeholder='Enter user name' />
              </FormControl>
              <FormControl>
                <FormLabel>Confirm User name</FormLabel>
                <Input placeholder='Confirm user name' />
              </FormControl>
            </ModalBody>
  
            <ModalFooter>
              <Button onClick={onClose}>Cancel</Button>
              {/* Disable delete user button when either field is blank or the fields don't match ? */}
              <Button 
              // onClick={deleteUser(user.id)}
              // colorScheme='blue' 
              mr={3}>
                Delete User
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </>
    )
  }

export default DeleteUserModal;
