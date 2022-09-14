import { Box, Text, VStack } from "@fidesui/react";
import { useAppSelector } from "app/hooks";
import { useAPIHelper } from "common/hooks";
import { useAlert } from "common/hooks/useAlert";
import { capitalize } from "common/utils";
import {
  selectConnectionTypeState,
  setConnection,
} from "connection-type/connection-type.slice";
import { ConnectionType } from "datastore-connections/constants";
import { usePatchDatastoreConnectionMutation } from "datastore-connections/datastore-connection.slice";
import { DatastoreConnectionRequest } from "datastore-connections/types";
import { useState } from "react";
import { useDispatch } from "react-redux";

import { BaseConnectorParametersFields } from "../types";
import ConnectorParametersForm from "./ConnectorParametersForm";

export const ConnectorParameters: React.FC = () => {
  const dispatch = useDispatch();
  const { errorAlert, successAlert } = useAlert();
  const { handleError } = useAPIHelper();
  const defaultValues = {
    description: "",
    name: "",
  } as BaseConnectorParametersFields;
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { connection, connectionOption } = useAppSelector(
    selectConnectionTypeState
  );

  const [patchDatastoreConnection] = usePatchDatastoreConnectionMutation();

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const handleSubmit = async (values: any, _actions: any) => {
    try {
      setIsSubmitting(true);
      const params1: DatastoreConnectionRequest = {
        access: "write",
        connection_type: connectionOption?.identifier as ConnectionType,
        description: values.description,
        disabled: false,
        name: values.name,
      };
      const payload = await patchDatastoreConnection(params1).unwrap();
      if (payload.failed?.length > 0) {
        errorAlert(payload.failed[0].message);
      } else {
        dispatch(setConnection(payload.succeeded[0]));
        successAlert(
          `Connector successfully ${connection?.key ? "updated" : "added"}!`
        );
      }
    } catch (error) {
      handleError(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <VStack align="stretch" gap="24px">
      <Box color="gray.700" fontSize="14px">
        To begin setting up your new {capitalize(connectionOption!.identifier)}
        connector you must first assign a name to the connector and a
        description. You must also assign an owner/s to this new connector so
        that they can be automatically contacted by their email when a new
        manual subject request has been received.
        <br />
        <br />
        Once you have completed this section you can then progress onto{" "}
        <Text display="inline-block" fontWeight="700">
          DSR customization
        </Text>{" "}
        using the menu on the right hand side.
      </Box>
      <ConnectorParametersForm
        defaultValues={defaultValues}
        isSubmitting={isSubmitting}
        onSaveClick={handleSubmit}
      />
    </VStack>
  );
};
