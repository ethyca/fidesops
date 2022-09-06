import {
  Alert,
  AlertDescription,
  AlertIcon,
  Box,
  Center,
  Spinner,
  useToast,
  VStack,
} from "@fidesui/react";
import { useAppSelector } from "app/hooks";
import { isErrorWithDetail, isErrorWithDetailArray } from "common/helpers";
import { capitalize } from "common/utils";
import { selectConnectionTypeState } from "connection-type/connection-type.slice";
import {
  useGetDatasetsQuery,
  usePatchDatasetMutation,
} from "datastore-connections/datastore-connection.slice";
import React, { useEffect, useRef, useState } from "react";

import YamlEditorForm from "./forms/YamlEditorForm";
import { replaceURL } from "./helpers";

const DatasetConfiguration: React.FC = () => {
  const mounted = useRef(false);
  const toast = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { connection, connectionOption, step } = useAppSelector(
    selectConnectionTypeState
  );
  const { data, isFetching, isLoading, isSuccess } = useGetDatasetsQuery(
    connection!.key
  );
  const [patchDataset] = usePatchDatasetMutation();

  const displayError = (content: string | JSX.Element) => {
    toast({
      position: "top",
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
      position: "top",
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

  const handleSubmit = async (value: any) => {
    try {
      setIsSubmitting(true);
      const params = {
        connection_key: connection?.key,
        items: [...value],
      };
      const payload = await patchDataset(params).unwrap();
      if (payload.failed?.length > 0) {
        displayError(payload.failed[0].message);
      } else {
        displaySuccess("Dataset successfully updated!");
      }
    } catch (error) {
      handleError(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  useEffect(() => {
    mounted.current = true;
    if (connection?.key) {
      replaceURL(connection.key, step.href);
    }
    return () => {
      mounted.current = false;
    };
  }, [connection?.key, step.href]);

  return (
    <VStack align="stretch" flex="1">
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
      {isSuccess && data!?.items ? (
        <YamlEditorForm
          data={data.items}
          isSubmitting={isSubmitting}
          onSubmit={handleSubmit}
        />
      ) : null}
    </VStack>
  );
};

export default DatasetConfiguration;
