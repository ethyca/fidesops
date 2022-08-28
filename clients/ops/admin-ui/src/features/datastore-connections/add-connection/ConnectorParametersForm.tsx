import {
  Button,
  ButtonGroup,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  Textarea,
  Tooltip,
  useToast,
  VStack,
} from "@fidesui/react";
import { useAppSelector } from "app/hooks";
import { isErrorWithDetail, isErrorWithDetailArray } from "common/helpers";
import { CircleHelpIcon } from "common/Icon";
import { capitalize } from "common/utils";
import { selectConnectionTypeState } from "connection-type/connection-type.slice";
import { ConnectionTypeSecretSchemaReponse } from "connection-type/types";
import { useLazyGetDatastoreConnectionStatusQuery } from "datastore-connections/datastore-connection.slice";
import { Field, Form, Formik } from "formik";
import React, { useEffect, useRef } from "react";

import { ConnectorParametersFormFields } from "./types";

const defaultValues: ConnectorParametersFormFields = {
  description: "",
  instance_key: "",
  name: "",
};

type ConnectorParametersFormProps = {
  data: ConnectionTypeSecretSchemaReponse;
  isSubmitting: boolean;
  onSaveClick: (values: any) => void;
  onTestConnectionClick: (value: any) => void;
};

const ConnectorParametersForm: React.FC<ConnectorParametersFormProps> = ({
  data,
  isSubmitting = false,
  onSaveClick,
  onTestConnectionClick,
}) => {
  const mounted = useRef(false);
  const toast = useToast();

  const { connectionKey, fidesKey, connectionOption } = useAppSelector(
    selectConnectionTypeState
  );

  const [trigger, result] = useLazyGetDatastoreConnectionStatusQuery();

  const validateField = (label: string, value: string) => {
    let error;
    if (!value) {
      error = `${label} is required`;
    }
    return error;
  };

  const getFormLabel = (id: string, value: string): JSX.Element => (
    <FormLabel
      color="gray.900"
      fontSize="14px"
      fontWeight="semibold"
      htmlFor={id}
      minWidth="141px"
    >
      {value}
    </FormLabel>
  );

  const getFormField = (key: string, item: { title: string }): JSX.Element => (
    <Field
      id={key}
      name={key}
      key={key}
      validate={
        data.required?.includes(key)
          ? (value: string) => validateField(item.title, value)
          : false
      }
    >
      {({ field, form }: { field: any; form: any }) => (
        <FormControl
          display="flex"
          isRequired={data.required?.includes(key)}
          isInvalid={form.errors[key] && form.touched[key]}
        >
          {getFormLabel(key, item.title)}
          <VStack align="flex-start" w="inherit">
            <Input {...field} autoComplete="off" color="gray.700" size="sm" />
            <FormErrorMessage>{form.errors[key]}</FormErrorMessage>
          </VStack>
          <CircleHelpIcon marginLeft="8px" visibility="hidden" />
        </FormControl>
      )}
    </Field>
  );

  const getInitialValues = () => {
    Object.entries(data.properties).forEach((key) => {
      defaultValues[key[0]] = "";
    });
    return defaultValues;
  };

  const handleError = (error: any) => {
    let errorMsg = "An unexpected error occurred. Please try again.";
    if (isErrorWithDetail(error)) {
      errorMsg = error.data.detail;
    } else if (isErrorWithDetailArray(error)) {
      errorMsg = error.data.detail[0].msg;
    }
    toast({
      status: "error",
      description: errorMsg,
    });
  };

  const handleSubmit = (values: any) => {
    onSaveClick(values);
  };

  const handleTestConnectionClick = async () => {
    try {
      await trigger(connectionKey).unwrap();
    } catch (error) {
      handleError(error);
    }
  };

  useEffect(() => {
    mounted.current = true;
    if (result.isSuccess) {
      onTestConnectionClick(result);
    }
    return () => {
      mounted.current = false;
    };
  }, [onTestConnectionClick, result]);

  return (
    <Formik
      initialValues={getInitialValues()}
      onSubmit={handleSubmit}
      validateOnBlur={false}
      validateOnChange={false}
    >
      <Form noValidate>
        <VStack align="stretch" gap="24px">
          {/* Name */}
          <Field
            id="name"
            name="name"
            validate={(value: string) => validateField("Name", value)}
          >
            {({ field, form }: { field: any; form: any }) => (
              <FormControl
                display="flex"
                isRequired
                isInvalid={form.errors.name && form.touched.name}
              >
                {getFormLabel("name", "Name")}
                <VStack align="flex-start" w="inherit">
                  <Input
                    {...field}
                    autoComplete="off"
                    autoFocus
                    color="gray.700"
                    placeholder={`Enter a friendly name for your new ${capitalize(
                      connectionOption!.identifier
                    )} connection`}
                    size="sm"
                  />
                  <FormErrorMessage>{form.errors.name}</FormErrorMessage>
                </VStack>
                <CircleHelpIcon marginLeft="8px" visibility="hidden" />
              </FormControl>
            )}
          </Field>
          {/* Description */}
          <Field id="description" name="description">
            {({ field }: { field: any }) => (
              <FormControl display="flex">
                {getFormLabel("description", "Description")}
                <Textarea
                  {...field}
                  color="gray.700"
                  placeholder={`Enter a description for your new ${capitalize(
                    connectionOption!.identifier
                  )} connection`}
                  resize="none"
                  size="sm"
                />
                <CircleHelpIcon marginLeft="8px" visibility="hidden" />
              </FormControl>
            )}
          </Field>
          {/* Connection Identifier */}
          <Field id="instance_key" name="instance_key">
            {({ field }: { field: any }) => (
              <FormControl display="flex" isRequired>
                {getFormLabel("instance_key", "Connection Identifier")}
                <Input
                  {...field}
                  autoComplete="off"
                  color="gray.700"
                  isDisabled={!!fidesKey}
                  placeholder={`A a unique identifier for your new ${capitalize(
                    connectionOption!.identifier
                  )} connection`}
                  size="sm"
                />
                <Tooltip
                  aria-label="The fides_key will allow fidesops to associate dataset field references appropriately. Must be a unique alphanumeric value with no spaces (underscores allowed) to represent this connection."
                  hasArrow
                  label="The fides_key will allow fidesops to associate dataset field references appropriately. Must be a unique alphanumeric value with no spaces (underscores allowed) to represent this connection."
                  placement="right-start"
                  openDelay={500}
                >
                  <CircleHelpIcon
                    marginLeft="8px"
                    _hover={{ cursor: "pointer" }}
                  />
                </Tooltip>
              </FormControl>
            )}
          </Field>
          {/* Dynamic connector secret fields */}
          {Object.entries(data.properties).map(([key, item]) =>
            getFormField(key, item)
          )}
          <ButtonGroup size="sm" spacing="8px" variant="outline">
            <Button
              colorScheme="gray.700"
              isDisabled={!connectionKey}
              isLoading={result.isLoading || result.isFetching}
              loadingText="Testing"
              onClick={handleTestConnectionClick}
              variant="outline"
            >
              Test connection
            </Button>
            <Button
              bg="primary.800"
              color="white"
              isLoading={isSubmitting}
              loadingText="Submitting"
              size="sm"
              variant="solid"
              type="submit"
              _active={{ bg: "primary.500" }}
              _disabled={{ opacity: "inherit" }}
              _hover={{ bg: "primary.400" }}
            >
              Save
            </Button>
          </ButtonGroup>
        </VStack>
      </Form>
    </Formik>
  );
};

export default ConnectorParametersForm;
