import {
  Button,
  ButtonGroup,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  Textarea,
  Tooltip,
  VStack,
} from "@fidesui/react";
import { CircleHelpIcon } from "common/Icon";
import { capitalize } from "common/utils";
import {
  ConnectionOption,
  ConnectionTypeSecretSchemaReponse,
} from "connection-type/types";
import { useLazyGetDatastoreConnectionStatusQuery } from "datastore-connections/datastore-connection.slice";
import { Field, Form, Formik } from "formik";
import React from "react";

import { CustomFields } from "../types";

const defaultValues: CustomFields = {
  name: "",
  description: "",
  connectionIdentifier: "",
};

type ConnectorParametersProps = {
  connectionOption: ConnectionOption;
  data: ConnectionTypeSecretSchemaReponse;
  onTestConnectionClick: (value: any) => void;
};

export const ConnectorParameters: React.FC<ConnectorParametersProps> = ({
  connectionOption,
  data,
  onTestConnectionClick,
}) => {
  const [trigger, result] = useLazyGetDatastoreConnectionStatusQuery();

  const getFormField = (key: string, item: { title: string }): JSX.Element => (
    <Field
      id={key}
      name={key}
      key={key}
      validate={
        data.required.includes(key)
          ? (value: string) => validateField(item.title, value)
          : false
      }
    >
      {({ field, form }: { field: any; form: any }) => (
        <FormControl
          display="flex"
          isRequired={data.required.includes(key)}
          isInvalid={form.errors[key] && form.touched[key]}
        >
          {getFormLabel(key, item.title)}
          <VStack align="flex-start" w="inherit">
            <Input {...field} color="gray.700" size="sm" />
            <FormErrorMessage>{form.errors[key]}</FormErrorMessage>
          </VStack>
          <CircleHelpIcon marginLeft="8px" />
        </FormControl>
      )}
    </Field>
  );

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

  const getInitialValues = () => {
    Object.entries(data.properties).forEach((key) => {
      defaultValues[key[0]] = "";
    });
    return defaultValues;
  };

  const handleSubmit = (values: any, actions: any) => {
    actions.setSubmitting(false);
  };

  const handleTestConnectionClick = () => {
    // TODO: Replace the connection key value with the
    // actual connection key value from the handleSubmit function
    // trigger("ci_create_test_data_datastore_connection_disabled").then(
    trigger("app_postgres_db").then((response) => {
      onTestConnectionClick(response);
    });
  };

  const validateField = (label: string, value: string) => {
    let error;
    if (!value) {
      error = `${label} is required`;
    }
    return error;
  };

  return (
    <Formik
      initialValues={getInitialValues()}
      onSubmit={handleSubmit}
      validateOnBlur={false}
    >
      {(props) => (
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
                      autoFocus
                      color="gray.700"
                      placeholder={`Enter a friendly name for your new ${capitalize(
                        connectionOption.identifier
                      )} connection`}
                      size="sm"
                    />
                    <FormErrorMessage>{form.errors.name}</FormErrorMessage>
                  </VStack>
                  <CircleHelpIcon marginLeft="8px" />
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
                      connectionOption.identifier
                    )} connection`}
                    resize="none"
                    size="sm"
                  />
                  <CircleHelpIcon marginLeft="8px" />
                </FormControl>
              )}
            </Field>
            {/* Connection Identifier */}
            <Field id="connectionIdentifier" name="connectionIdentifier">
              {({ field }: { field: any }) => (
                <FormControl display="flex">
                  {getFormLabel(
                    "connectionIdentifier",
                    "Connection Identifier"
                  )}
                  <Input
                    {...field}
                    color="gray.700"
                    placeholder={`A a unique identifier for your new ${capitalize(
                      connectionOption.identifier
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
            {/* Dynamic custom fields */}
            {Object.entries(data.properties).map(([key, item]) =>
              getFormField(key, item)
            )}
            <ButtonGroup size="sm" spacing="8px" variant="outline">
              <Button
                colorScheme="gray.700"
                isDisabled={!props.isValid}
                isLoading={result.isLoading || result.isFetching}
                loadingText="Testing"
                onClick={handleTestConnectionClick}
                variant="outline"
                _disabled={{ opacity: "inherit" }}
              >
                Test connection
              </Button>
              <Button
                bg="primary.800"
                color="white"
                isLoading={props.isSubmitting}
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
      )}
    </Formik>
  );
};
