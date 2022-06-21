import {
  Button,
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
} from "@fidesui/react";
import React from "react";

import { useDeleteDatastoreConnectionMutation } from "./datastore-connection.slice";

type DataConnectionProps = {
  connection_key: string;
};

const DeleteConnectionModal: React.FC<DataConnectionProps> = ({
  connection_key,
}) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [deleteConnection] = useDeleteDatastoreConnectionMutation();

  const handleDeleteConnection = () => {
    if (connection_key) {
      deleteConnection(connection_key);
      onClose();
    }
  };

  return (
    <>
      <MenuItem
        _focus={{ color: "complimentary.500", bg: "gray.100" }}
        onClick={onOpen}
      >
        <Text fontSize="sm">Delete</Text>
      </MenuItem>
      <Modal isCentered isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Delete Connection</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <Stack direction="column" spacing="15px">
              <Text
                color="gray.600"
                fontSize="sm"
                fontWeight="sm"
                lineHeight="20px"
              >
                Deleting a datastore connection may impact any subject request
                that is currently in progress. Do you wish to proceed?
              </Text>
            </Stack>
          </ModalBody>

          <ModalFooter>
            <Button
              onClick={onClose}
              marginRight="10px"
              size="sm"
              variant="solid"
              bg="white"
              width="50%"
            >
              Cancel
            </Button>
            <Button
              onClick={handleDeleteConnection}
              mr={3}
              size="sm"
              variant="solid"
              bg="primary.800"
              color="white"
              width="50%"
            >
              Delete Connection
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
};

export default DeleteConnectionModal;
