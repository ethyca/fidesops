import React from "react";
import {
  ModalHeader,
  ModalFooter,
  ModalBody,
  Text,
  Button,
} from "@fidesui/react";


type RequestSubmittedProps = {
  onClose: () => void;
  action: any;
};

const RequestSubmitted: React.FC<RequestSubmittedProps> = ({
  onClose,
  action,
}) => (
    <>
      <ModalHeader pt={6} pb={0}>
        Request submitted
      </ModalHeader>

      <ModalBody>
        <Text fontSize="sm" color="gray.500" mb={4}>
          Thanks for your {action.policy_key} Request. A member of our team will
          review and be in contact with you shortly.
        </Text>
      </ModalBody>

      <ModalFooter pb={6}>
        <Button
          flex="1"
          bg="primary.800"
          _hover={{ bg: "primary.400" }}
          _active={{ bg: "primary.500" }}
          colorScheme="primary"
          size="sm"
          onClick={onClose}
        >
          Continue
        </Button>
      </ModalFooter>
    </>
  );

export default RequestSubmitted;
