import { Box, VStack } from "@fidesui/react";
import { useAppSelector } from "app/hooks";
import { useAlert, useAPIHelper } from "common/hooks";
import { selectConnectionTypeState } from "connection-type/connection-type.slice";
import { useCreateAccessManualWebhookMutation } from "datastore-connections/datastore-connection.slice";
import React, { useState } from "react";

import DSRCustomizationForm from "./DSRCustomizationForm";
import { Field } from "./types";

const DSRCustomization: React.FC = () => {
  const { successAlert } = useAlert();
  const { handleError } = useAPIHelper();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { connection } = useAppSelector(selectConnectionTypeState);

  const [createAccessManualWebhook] = useCreateAccessManualWebhookMutation();

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const handleSubmit = async (values: Field[], _actions: any) => {
    try {
      setIsSubmitting(true);
      const params = {
        connection_key: connection?.key as string,
        body: { ...values },
      };
      await createAccessManualWebhook(params).unwrap();
      successAlert("DSR customization saved");
    } catch (error) {
      handleError(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <VStack align="stretch" gap="24px">
      <Box color="gray.700" fontSize="14px" w="572px">
        Below you can select the required PII for this manually setup
        Integration and then choose to remap a custom label for the DSR package
        your users will download etc.
      </Box>
      <DSRCustomizationForm
        isSubmitting={isSubmitting}
        onSaveClick={handleSubmit}
      />
    </VStack>
  );
};

export default DSRCustomization;
