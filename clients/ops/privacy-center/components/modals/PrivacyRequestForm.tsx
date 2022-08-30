import React, { useEffect, useState } from "react";
import {
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
} from "@fidesui/react";

import { useFormik } from "formik";

import type { AlertState } from "../../types/AlertState";

import config from "../../config/config.json";

const usePrivacyRequestForm = ({
  onClose,
  action,
  setAlert,
}: {
  onClose: () => void;
  action: typeof config.actions[0] | null;
  setAlert: (state: AlertState) => void;
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const formik = useFormik({
    initialValues: {
      name: "",
      email: "",
      phone: "",
    },
    onSubmit: async (values) => {
      if (!action) {
        // somehow we've reached a broken state, return
        return;
      }

      setIsLoading(true);
      const host =
        process.env.NODE_ENV === "development"
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

      const handleError = () => {
        setAlert({
          status: "error",
          description: "Your request has failed. Please try again.",
        });
        onClose();
      };

      try {
        const response = await fetch(`${host}/privacy-request`, {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            "X-Fides-Source": "fidesops-privacy-center",
          },
          body: JSON.stringify(body),
        });

        if (!response.ok) {
          handleError();
          return;
        }

        const data = await response.json();

        if (data.succeeded.length) {
          setAlert({
            status: "success",
            description:
              "Your request was successful, please await further instructions.",
          });
        } else {
          handleError();
        }
      } catch (error) {
        handleError();
        return;
      }

      onClose();
    },
    validate: (values) => {
      if (!action) return {};
      const errors: {
        name?: string;
        email?: string;
        phone?: string;
      } = {};

      if (!values.email && action.identity_inputs.email === "required") {
        errors.email = "Required";
      }

      if (!values.name && action.identity_inputs.name === "required") {
        errors.name = "Required";
      }

      if (!values.phone && action.identity_inputs.phone === "required") {
        errors.phone = "Required";
      }

      return errors;
    },
  });

  return { ...formik, isLoading };
};

export const PrivacyRequestForm: React.FC<{
  isOpen: boolean;
  onClose: () => void;
  openAction: string | null;
  setAlert: (state: AlertState) => void;
}> = ({ isOpen, onClose, openAction, setAlert }) => {
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
    resetForm,
  } = usePrivacyRequestForm({ onClose, action, setAlert });

  useEffect(() => resetForm(), [isOpen, resetForm]);

  if (!action) return null;

  return (
    <>
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
                  placeholder={
                    action.identity_inputs.name === "required"
                      ? "Name*"
                      : "Name"
                  }
                  isRequired={action.identity_inputs.name === "required"}
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
                  placeholder={
                    action.identity_inputs.email === "required"
                      ? "Email*"
                      : "Email"
                  }
                  isRequired={action.identity_inputs.email === "required"}
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
                  placeholder={
                    action.identity_inputs.phone === "required"
                      ? "Phone*"
                      : "Phone"
                  }
                  isRequired={action.identity_inputs.phone === "required"}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  value={values.phone}
                  isInvalid={touched.phone && Boolean(errors.phone)}
                />
                <FormErrorMessage>{errors.phone}</FormErrorMessage>
              </FormControl>
            ) : null}
          </Stack>
        </ModalBody>

        <ModalFooter pb={6}>
          <Button variant="outline" flex="1" mr={3} size="sm" onClick={onClose}>
            Cancel
          </Button>
          <Button
            type="submit"
            flex="1"
            bg="primary.800"
            _hover={{ bg: "primary.400" }}
            _active={{ bg: "primary.500" }}
            colorScheme="primary"
            disabled={!(isValid && dirty)}
            size="sm"
          >
            Continue
          </Button>
        </ModalFooter>
      </chakra.form>
    </>
  );
};
