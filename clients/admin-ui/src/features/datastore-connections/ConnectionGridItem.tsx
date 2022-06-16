import { Box, Button, Flex, Spacer, Text } from "@fidesui/react";
import { format } from "date-fns-tz";
import React from "react";

import ConnectionMenu from "./ConnectionMenu";
import ConnectionStatusBadge from "./ConnectionStatusBadge";
import { useLazyGetDatastoreConnectionStatusQuery } from "./datastore-connection.slice";
import { DatastoreConnection } from "./types";

type ConnectionGridItemProps = {
  connectionData: DatastoreConnection;
};

const ConnectionGridItem: React.FC<ConnectionGridItemProps> = ({
  connectionData,
}) => {
  useLazyGetDatastoreConnectionStatusQuery();
  const [trigger, result, lastPromiseInfo] =
    useLazyGetDatastoreConnectionStatusQuery();

  return (
    <Box
      width="100%"
      height={136}
      border="1px"
      borderColor="blackAlpha.300"
      boxSizing="border-box"
      p="18px 16px 16px 16px"
    >
      <Flex justifyContent="center" alignItems="center">
        <Box width="32px" height="32px" backgroundColor="aliceblue" />
        <Text
          color="gray.900"
          fontSize="md"
          fontWeight="medium"
          m="8px"
          lineHeight="24px"
        >
          {connectionData.name}
        </Text>
        <Spacer />
        <ConnectionStatusBadge disabled={connectionData.disabled} />
        <ConnectionMenu />
      </Flex>
      <Text color="gray.600" fontSize="sm" fontWeight="sm" lineHeight="20px">
        {/* {data.connection_type} Database Connector */}
        Mailchimp Saas Connector
      </Text>
      <Text color="gray.600" fontSize="sm" fontWeight="sm" lineHeight="20px">
        Edited on{" "}
        {format(new Date(connectionData.updated_at!), "MMMM d, Y, KK:mm:ss z")}
      </Text>

      <Flex mt="0px" justifyContent="center" alignItems="center">
        <Box
          width="12px"
          height="12px"
          borderRadius="6px"
          backgroundColor={
            connectionData.last_test_succeeded ? "green.500" : "red.500"
          }
        />
        <Text
          color="gray.500"
          fontSize="xs"
          fontWeight="semibold"
          lineHeight="16px"
          ml="10px"
        >
          Last tested on{" "}
          {format(
            new Date(connectionData.last_test_timestamp!),
            "MMMM d, Y, KK:mm:ss z"
          )}
        </Text>
        <Spacer />
        <Button
          size="xs"
          variant="outline"
          onClick={() => {
            trigger(connectionData.key);
          }}
          loadingText="Test"
          isLoading={result.isLoading || result.isFetching}
          spinnerPlacement="end"
        >
          Test
        </Button>
      </Flex>
    </Box>
  );
};

export default ConnectionGridItem;
