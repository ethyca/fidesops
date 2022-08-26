import { Box, Center, Spinner, useToast, VStack } from "@fidesui/react";
import { useAppSelector } from "app/hooks";
import { isErrorWithDetail, isErrorWithDetailArray } from "common/helpers";
import { capitalize } from "common/utils";
import { selectConnectionTypeState } from "connection-type/connection-type.slice";
import { useGetDatasetQuery } from "datastore-connections/datastore-connection.slice";
import React, { useState } from "react";

import YamlEditorForm from "../YamlEditorForm";

const DatasetConfiguration: React.FC = () => {
  const toast = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { connectionKey, connectionOption, fidesKey, step } = useAppSelector(
    selectConnectionTypeState
  );
  const { data, isFetching, isLoading, isSuccess } = useGetDatasetQuery({
    connection_key: connectionKey,
    fides_key: fidesKey,
  });

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

  const handleSubmit = (value: Object) => {
    console.log(value)
    setIsSubmitting(true);
    // eslint-disable-next-line no-empty
    try {
    } catch (error) {
      handleError(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <VStack align="stretch">
      <Box color="gray.700" fontSize="14px" w="475px" mb={4}>
        {step.description?.replace(
          "{identifier}",
          capitalize(connectionOption!.identifier)
        )}
      </Box>
      {(isFetching || isLoading) && (
        <Center>
          <Spinner />
        </Center>
      )}
      {isSuccess ? (
        <YamlEditorForm
          data={data}
          isSubmitting={isSubmitting}
          onSubmit={handleSubmit}
        />
      ) : null}
    </VStack>
  );
};

export default DatasetConfiguration;
