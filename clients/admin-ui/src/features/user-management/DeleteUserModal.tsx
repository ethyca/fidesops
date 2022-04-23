import {
    Button,
    FormControl,
    FormLabel,
    Input,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    useDisclosure,
  } from '@fidesui/react';

function DeleteUserModal() {
    const { isOpen, onOpen, onClose } = useDisclosure()
  
    return (
      <>
        <Button onClick={onOpen}>Delete</Button>
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
              <Button colorScheme='blue' mr={3}>
                Delete User
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </>
    )
  }

export default DeleteUserModal;
