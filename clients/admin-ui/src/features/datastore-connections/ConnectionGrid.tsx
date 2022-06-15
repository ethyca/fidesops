import { SimpleGrid, Spinner } from "@fidesui/react";

import ConnectionGridItem from "./ConnectionGridItem";
import { useGetAllDatastoreConnectionsQuery } from "./datastore-connection.slice";
import { temp } from "./types";

// type ConnectionGridProps = {};

const ConnectionGrid: React.FC = () => {
  const { data, isUninitialized, isLoading } =
    useGetAllDatastoreConnectionsQuery(temp);
  console.log(data);
  if (isUninitialized || isLoading) {
    return <Spinner />;
  }

  const test = [
    data!.items[0],
    data!.items[0],
    data!.items[0],
    data!.items[0],
    data!.items[0],
    data!.items[0],
    data!.items[0],
    data!.items[0],
    data!.items[0],
    data!.items[0],
  ];
  const gridItems = test.map((d, idx) => (
    <ConnectionGridItem key={d.key + idx} data={d} />
  ));
  return (
    <SimpleGrid minChildWidth={400} columns={3} spacing={0}>
      {gridItems}
    </SimpleGrid>
  );
};

export default ConnectionGrid;
