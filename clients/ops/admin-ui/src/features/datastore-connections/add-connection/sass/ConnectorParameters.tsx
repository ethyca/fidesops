import { useToast } from "@fidesui/react";
import { useAppSelector } from "app/hooks";
import { isErrorWithDetail, isErrorWithDetailArray } from "common/helpers";
import {
  selectConnectionTypeState,
  setConnectionKey,
  setFidesKey,
} from "connection-type/connection-type.slice";
import { ConnectionTypeSecretSchemaReponse } from "connection-type/types";
import { SaasType } from "datastore-connections/constants";
import { useCreateSassConnectionConfigMutation } from "datastore-connections/datastore-connection.slice";
import { SassConnectionConfigRequest } from "datastore-connections/types";
import React, { useState } from "react";
import { useDispatch } from "react-redux";

import ConnectorParametersForm from "../ConnectorParametersForm";

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

  const { connectionOption } = useAppSelector(selectConnectionTypeState);
  const [createSassConnectionConfig] = useCreateSassConnectionConfigMutation();

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
      dispatch(setConnectionKey(payload.connection.key));
      dispatch(setFidesKey(payload.dataset.fides_key));
      toast({
        status: "success",
        description: "Connector successfully added!",
      });
    } catch (error) {
      handleError(error);
    } finally {
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
