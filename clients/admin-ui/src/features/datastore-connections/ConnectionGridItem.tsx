import { Box, Button, Flex, Image, Spacer, Text } from "@fidesui/react";
import { format } from "date-fns-tz";
import React from "react";

import { capitalize } from "../common/utils";
import ConnectionMenu from "./ConnectionMenu";
import ConnectionStatusBadge from "./ConnectionStatusBadge";
import {
  ConnectionTypeImageMap,
  CONNECTOR_IMAGE_PATH,
  FALLBACK_CONNECTOR_IMAGE_PATH
} from "./constants";
import { useLazyGetDatastoreConnectionStatusQuery } from "./datastore-connection.slice";
import { ConnectionType, DatastoreConnection } from "./types";

type TestDataProps = {
  succeeded: boolean | null;
  timestamp: string;
};

const TestData: React.FC<TestDataProps> = ({ succeeded, timestamp }) => {
  let testCircleColor = succeeded ? "green.500" : "red.500";
  if (succeeded === null) {
    testCircleColor = "gray.300";
  }

  const date = format(new Date(timestamp), "MMMM d, Y, KK:mm:ss z");
  const testText = timestamp
    ? `Last tested on ${date}`
    : "This datastore has not been tested yet";

  return (
    <>
      <Box
        width="12px"
        height="12px"
        borderRadius="6px"
        backgroundColor={testCircleColor}
      />
      <Text
        color="gray.500"
        fontSize="xs"
        fontWeight="semibold"
        lineHeight="16px"
        ml="10px"
      >
        {testText}
      </Text>
    </>
  );
};

const useConnectionGridItem = () => {
  const getConnectorDisplayName = (connectionType: ConnectionType): string => {
    if (Object.values(ConnectionType).includes(connectionType)) {
      return `${capitalize(connectionType)} Database Connector`;
    }

    let value: string;
    switch (connectionType) {
      case ConnectionType.HTTPS:
        value = "HTTPS Connector";
        break;
      case ConnectionType.MANUAL:
        value = "Manual Connector";
        break;
      case ConnectionType.SAAS:
        value = "Sass Connector";
        break;
      default:
        value = "Unknown Connector";
        break;
    }

    return value;
  };

  const getImageSrc = (connectionType: string): string => {
    const item = [...ConnectionTypeImageMap].find(
      ([k]) => k.toLowerCase() === connectionType.toLowerCase()
    );
    const path = item
      ? CONNECTOR_IMAGE_PATH + item[1]
      : FALLBACK_CONNECTOR_IMAGE_PATH;
    return path;
  };

  return {
    getConnectorDisplayName,
    getImageSrc,
  };
};

type ConnectionGridItemProps = {
  connectionData: DatastoreConnection;
};

const ConnectionGridItem: React.FC<ConnectionGridItemProps> = ({
  connectionData,
}) => {
  const [trigger, result] = useLazyGetDatastoreConnectionStatusQuery();
  const { getConnectorDisplayName, getImageSrc } = useConnectionGridItem();

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
        <Image
          boxSize="32px"
          objectFit="cover"
          src={getImageSrc(connectionData.connection_type)}
          fallbackSrc={FALLBACK_CONNECTOR_IMAGE_PATH}
          alt={connectionData.name}
        />
        <Text
          color="gray.900"
          fontSize="md"
          fontWeight="medium"
          m="8px"
          textOverflow="ellipsis"
          overflow="hidden"
          whiteSpace="nowrap"
        >
          {connectionData.name}
        </Text>
        <Spacer />
        <ConnectionStatusBadge disabled={connectionData.disabled} />
        <ConnectionMenu
          connection_key={connectionData.key}
          disabled={connectionData.disabled}
          name={connectionData.name}
          connection_type={connectionData.connection_type}
          access_type={connectionData.access}
        />
      </Flex>
      <Text color="gray.600" fontSize="sm" fontWeight="sm" lineHeight="20px">
        {getConnectorDisplayName(connectionData.connection_type)}
      </Text>
      <Text color="gray.600" fontSize="sm" fontWeight="sm" lineHeight="20px">
        Edited on{" "}
        {format(new Date(connectionData.updated_at!), "MMMM d, Y, KK:mm:ss z")}
      </Text>

      <Flex mt="0px" justifyContent="center" alignItems="center">
        <TestData
          succeeded={connectionData.last_test_succeeded}
          timestamp={connectionData.last_test_timestamp}
        />
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
