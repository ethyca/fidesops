import { Button, Flex, SimpleGrid, Spinner, Text } from "@fidesui/react";
import React from "react";

import ConnectionGridItem from "./ConnectionGridItem";
import { useGetAllDatastoreConnectionsQuery } from "./datastore-connection.slice";
import { temp } from "./types";

const ConnectionGrid: React.FC = () => {
  const { data, isUninitialized, isLoading } =
    useGetAllDatastoreConnectionsQuery(temp);
  if (isUninitialized || isLoading) {
    return <Spinner />;
  }

  let body = (
    <Flex
      bg="gray.50"
      width="100%"
      height="340px"
      justifyContent="center"
      alignItems="center"
      flexDirection="column"
    >
      <Text
        color="black"
        fontSize="x-large"
        lineHeight="32px"
        fontWeight="600"
        mb="7px"
      >
        Welcome to your Datastore!
      </Text>
      <Text color="gray.600" fontSize="sm" lineHeight="20px" mb="11px">
        You don't have any Connections set up yet.
      </Text>
      <Button
        variant="solid"
        bg="primary.800"
        color="white"
        flexShrink={0}
        size="sm"
      >
        Create New Connection
      </Button>
    </Flex>
  );

  // @ts-ignore
  if (data?.items.length > 0) {
    const gridItems = data!.items.map((d, idx) => (
      <ConnectionGridItem key={d.key + idx} connectionData={d} />
    ));
    body = (
      <SimpleGrid minChildWidth={400} columns={3} spacing={0}>
        {gridItems}
      </SimpleGrid>
    );
  }

  return body;
};

export default ConnectionGrid;
