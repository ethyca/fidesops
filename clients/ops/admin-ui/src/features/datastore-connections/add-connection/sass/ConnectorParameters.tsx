import { useToast } from "@fidesui/react";
import { useAppSelector } from "app/hooks";
import { isErrorWithDetail, isErrorWithDetailArray } from "common/helpers";
import {
  selectConnectionTypeState,
  setConnection,
} from "connection-type/connection-type.slice";
import { ConnectionTypeSecretSchemaReponse } from "connection-type/types";
import { SaasType } from "datastore-connections/constants";
import {
  useCreateSassConnectionConfigMutation,
  usePatchDatastoreConnectionMutation,
  useUpdateDatastoreConnectionSecretsMutation,
} from "datastore-connections/datastore-connection.slice";
import {
  DatastoreConnectionRequest,
  DatastoreConnectionSecretsRequest,
  SassConnectionConfigRequest,
} from "datastore-connections/types";
import React, { useState } from "react";
import { useDispatch } from "react-redux";

import ConnectorParametersForm from "../forms/ConnectorParametersForm";
import { replaceURL } from "../helpers";

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
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { connection, connectionOption, step } = useAppSelector(
    selectConnectionTypeState
  );

  const [createSassConnectionConfig] = useCreateSassConnectionConfigMutation();
  const [patchDatastoreConnection] = usePatchDatastoreConnectionMutation();
  const [updateDatastoreConnectionSecrets] =
    useUpdateDatastoreConnectionSecretsMutation();

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

  const handleSubmit = async (values: any) => {
    try {
      setIsSubmitting(true);
      if (connection) {
        // Update existing Sass connector
        const params1: DatastoreConnectionRequest = {
          access: "read",
          connection_type: connection.connection_type,
          description: values.description,
          disabled: false,
          key: connection.key,
          name: values.name,
        };
        const params2: DatastoreConnectionSecretsRequest = {
          connection_key: connection.key,
          secrets: {},
        };
        Object.entries(data.properties).forEach((key) => {
          params2.secrets[key[0]] = values[key[0]];
        });
        Promise.all([
          patchDatastoreConnection(params1),
          updateDatastoreConnectionSecrets(params2),
        ])
          .then(() => {
            toast({
              status: "success",
              description: `Connector successfully updated!`,
            });
            setIsSubmitting(false);
          })
          .catch((error) => {
            throw error;
          });
      } else {
        // Create new Sass connector
        const params: SassConnectionConfigRequest = {
          description: values.description,
          instance_key: (values.instance_key as string)
            .toLowerCase()
            .replace(/ /g, "_"),
          name: values.name,
          saas_connector_type: connectionOption!.identifier as SaasType,
          secrets: {},
        };
        Object.entries(data.properties).forEach((key) => {
          params.secrets[key[0]] = values[key[0]];
        });
        const payload = await createSassConnectionConfig(params).unwrap();
        dispatch(setConnection(payload.connection));
        // Update the current browser url with the new key created
        replaceURL(payload.connection.key, step.href);
        toast({
          status: "success",
          description: `Connector successfully added!`,
        });
        setIsSubmitting(false);
      }
    } catch (error) {
      handleError(error);
      setIsSubmitting(false);
    }
  };

  return (
    <ConnectorParametersForm
      data={data}
      isSubmitting={isSubmitting}
      onSaveClick={handleSubmit}
      onTestConnectionClick={onTestConnectionClick}
    />
  );
};
