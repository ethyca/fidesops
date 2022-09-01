import {
  Alert,
  AlertDescription,
  AlertIcon,
  Box,
  useToast,
} from "@fidesui/react";
import { useAppSelector } from "app/hooks";
import { isErrorWithDetail, isErrorWithDetailArray } from "common/helpers";
import {
  selectConnectionTypeState,
  setConnection,
} from "connection-type/connection-type.slice";
import { ConnectionTypeSecretSchemaReponse } from "connection-type/types";
import { ConnectionType } from "datastore-connections/constants";
import {
  usePatchDatastoreConnectionMutation,
  useUpdateDatastoreConnectionSecretsMutation,
} from "datastore-connections/datastore-connection.slice";
import {
  DatastoreConnectionRequest,
  DatastoreConnectionSecretsRequest,
} from "datastore-connections/types";
import { useState } from "react";
import { useDispatch } from "react-redux";

import ConnectorParametersForm from "../forms/ConnectorParametersForm";
import { formatKey } from "../helpers";
import { DatabaseConnectorParametersFormFields } from "../types";

type ConnectorParametersProps = {
  data: ConnectionTypeSecretSchemaReponse;
  onTestConnectionClick: (value: any) => void;
};

export const ConnectorParameters: React.FC<ConnectorParametersProps> = ({
  data,
  onTestConnectionClick,
}) => {
  const dispatch = useDispatch();
  const toast = useToast();
  const defaultValues = {
    description: "",
    instance_key: "",
    name: "",
  } as DatabaseConnectorParametersFormFields;
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { connection, connectionOption } = useAppSelector(
    selectConnectionTypeState
  );

  const [patchDatastoreConnection] = usePatchDatastoreConnectionMutation();
  const [updateDatastoreConnectionSecrets] =
    useUpdateDatastoreConnectionSecretsMutation();

  const displayError = (content: string | JSX.Element) => {
    toast({
      render: () => (
        <Alert status="error">
          <AlertIcon />
          <Box>
            <AlertDescription>{content}</AlertDescription>
          </Box>
        </Alert>
      ),
    });
  };

  const displaySuccess = (content: string) => {
    toast({
      render: () => (
        <Alert status="success" variant="subtle">
          <AlertIcon />
          {content}
        </Alert>
      ),
    });
  };

  const handleError = (error: any) => {
    let errorMsg = "An unexpected error occurred. Please try again.";
    if (isErrorWithDetail(error)) {
      errorMsg = error.data.detail;
    } else if (isErrorWithDetailArray(error)) {
      errorMsg = error.data.detail[0].msg;
    }
    displayError(errorMsg);
  };

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const handleSubmit = async (values: any, _actions: any) => {
    try {
      setIsSubmitting(true);
      const params1: DatastoreConnectionRequest = {
        access: "write",
        connection_type: connectionOption?.identifier as ConnectionType,
        description: values.description,
        disabled: false,
        key: formatKey(values.instance_key as string),
        name: values.name,
      };
      const payload = await patchDatastoreConnection(params1).unwrap();
      if (payload.failed?.length > 0) {
        displayError(payload.failed[0].message);
      } else {
        dispatch(setConnection(payload.succeeded[0]));
        const params2: DatastoreConnectionSecretsRequest = {
          connection_key: payload.succeeded[0].key,
          secrets: {},
        };
        Object.entries(data.properties).forEach((key) => {
          params2.secrets[key[0]] = values[key[0]];
        });
        const payload2 = await updateDatastoreConnectionSecrets(
          params2
        ).unwrap();
        if (payload2.test_status === "failed") {
          displayError(
            <>
              <b>Message:</b> {payload2.msg}
              <br />
              <b>Failure Reason:</b> {payload2.failure_reason}
            </>
          );
        } else {
          displaySuccess(
            `Connector successfully ${connection?.key ? "updated" : "added"}!`
          );
        }
      }
    } catch (error) {
      handleError(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <ConnectorParametersForm
      data={data}
      defaultValues={defaultValues}
      isSubmitting={isSubmitting}
      onSaveClick={handleSubmit}
      onTestConnectionClick={onTestConnectionClick}
    />
  );
};
