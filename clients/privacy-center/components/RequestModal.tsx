import React, { useState } from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  Text,
  Button,
  chakra,
  Stack,
  FormControl,
  Input,
  FormErrorMessage,
} from '@fidesui/react';

import { useFormik } from 'formik';

import config from '../config/config.json';

export const useRequestModal = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [openAction, setOpenAction] = useState<string | null>(null);

  const onOpen = (action: string) => {
    setIsOpen(true);
    setOpenAction(action);
  };

  const onClose = () => {
    setIsOpen(false);
  };

  return { isOpen, onClose, onOpen, openAction };
};

const useRequestForm = ({
  onClose,
  action,
}: {
  onClose: () => void;
  action: typeof config.actions[0] | null;
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const formik = useFormik({
    initialValues: {
      name: '',
      email: '',
      phone: '',
    },
    onSubmit: async (values) => {
      if (!action) {
        // somehow we've reached a broken state, return
        return;
      }

      setIsLoading(true);
      const host =
        process.env.NODE_ENV === 'development'
          ? config.fidesops_host_development
          : config.fidesops_host_production;
      const body = [
        {
          identity: {
            email: values.email,
            phone_number: values.phone,
            // enable this when name field is supported on the server
            // name: values.name
          },
          policy_key: action.policy_key,
        },
      ];
      const response = await fetch(`${host}/privacy-request`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });
      const data = await response.json();
      console.log(data);
      onClose();
    },
    validate: (values) => {
      const errors: {
        name?: string;
        email?: string;
        phone?: string;
      } = {};

      if (!values.email) {
        errors.email = 'Required';
      } else if (
        !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)
      ) {
        errors.email = 'Invalid email address';
      }

      if (!values.name) {
        errors.name = 'Required';
      }

      return errors;
    },
  });

  return { ...formik, isLoading };
};

export const RequestModal: React.FC<{
  isOpen: boolean;
  onClose: () => void;
  openAction: string | null;
}> = ({ isOpen, onClose, openAction }) => {
  const action = openAction
    ? config.actions.filter(({ policy_key }) => policy_key === openAction)[0]
    : null;
  const {
    errors,
    handleBlur,
    handleChange,
    handleSubmit,
    touched,
    values,
    isValid,
    dirty,
  } = useRequestForm({ onClose, action });
  if (!action) return null;
  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent top={[0, '205px']} maxWidth="464px" mx={5} my={3}>
        <ModalHeader pt={6} pb={0}>
          {action.title}
        </ModalHeader>
        <chakra.form onSubmit={handleSubmit}>
          <ModalBody>
            <Text fontSize="sm" color="gray.500" mb={4}>
              {action.description}
            </Text>
            <Stack spacing={3}>
              {action.identity_inputs.name ? (
                <FormControl
                  id="name"
                  isInvalid={touched.name && Boolean(errors.name)}
                >
                  <Input
                    id="name"
                    name="name"
                    focusBorderColor="primary.500"
                    placeholder="Name*"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.name}
                    isInvalid={touched.name && Boolean(errors.name)}
                  />
                  <FormErrorMessage>{errors.name}</FormErrorMessage>
                </FormControl>
              ) : null}
              {action.identity_inputs.email ? (
                <FormControl
                  id="email"
                  isInvalid={touched.email && Boolean(errors.email)}
                >
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    focusBorderColor="primary.500"
                    placeholder="Email*"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.email}
                    isInvalid={touched.email && Boolean(errors.email)}
                  />
                  <FormErrorMessage>{errors.email}</FormErrorMessage>
                </FormControl>
              ) : null}
              {action.identity_inputs.phone ? (
                <FormControl
                  id="phone"
                  isInvalid={touched.phone && Boolean(errors.phone)}
                >
                  <Input
                    id="phone"
                    name="phone"
                    type="phone"
                    focusBorderColor="primary.500"
                    placeholder="Phone"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.phone}
                    isInvalid={touched.phone && Boolean(errors.phone)}
                  />
                  {/* <FormErrorMessage>{errors.phone}</FormErrorMessage> */}
                </FormControl>
              ) : null}
            </Stack>
          </ModalBody>

          <ModalFooter pb={6}>
            <Button variant="outline" flex="1" mr={3} onClick={onClose}>
              Cancel
            </Button>
            <Button
              type="submit"
              flex="1"
              colorScheme="primary"
              disabled={!(isValid && dirty)}
            >
              Continue
            </Button>
          </ModalFooter>
        </chakra.form>
      </ModalContent>
    </Modal>
  );
};
