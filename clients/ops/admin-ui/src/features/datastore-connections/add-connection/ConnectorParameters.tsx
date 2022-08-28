import { Box, Center, Flex, Spinner, VStack } from "@fidesui/react";
import { useAppSelector } from "app/hooks";
import { capitalize } from "common/utils";
import {
  selectConnectionTypeState,
  useGetConnectionTypeSecretSchemaQuery,
} from "connection-type/connection-type.slice";
import { SystemType } from "datastore-connections/constants";
import React, { useState } from "react";

import { ConnectorParameters as DatabaseConnectorParameters } from "./database/ConnectorParameters";
import { ConnectorParameters as SassConnectorParameters } from "./sass/ConnectorParameters";
import TestConnection from "./TestConnection";

export const ConnectorParameters: React.FC = () => {
  const { connectionOption, step } = useAppSelector(selectConnectionTypeState);

  const { data, isFetching, isLoading, isSuccess } =
    useGetConnectionTypeSecretSchemaQuery(connectionOption!.identifier);
  const [response, setResponse] = useState<any>();

  const handleTestConnectionClick = (value: any) => {
    setResponse(value);
  };

  return (
    <Flex gap="97px">
      <VStack w="579px" gap="24px" align="stretch">
        <Box color="gray.700" fontSize="14px" h="80px" w="475px">
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
        {connectionOption?.type === SystemType.DATABASE && isSuccess && data ? (
          <DatabaseConnectorParameters
            data={data}
            onTestConnectionClick={handleTestConnectionClick}
          />
        ) : null}
        {connectionOption?.type === SystemType.SAAS && isSuccess && data ? (
          <SassConnectorParameters
            data={data}
            onTestConnectionClick={handleTestConnectionClick}
          />
        ) : null}
      </VStack>
      {response && (
        <Box w="480px" mt="16px">
          <TestConnection response={response} />
        </Box>
      )}
    </Flex>
  );
};

export default ConnectorParameters;
