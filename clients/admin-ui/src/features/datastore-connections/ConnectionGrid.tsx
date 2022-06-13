import { Grid, Spinner } from '@fidesui/react';

import ConnectionGridItem from './ConnectionGridItem';
import { useGetAllDatastoreConnectionsQuery } from './datastore-connection.slice';
import { temp } from './types';

// type ConnectionGridProps = {};

const ConnectionGrid: React.FC = () => {
  const { data, isUninitialized, isLoading } =
    useGetAllDatastoreConnectionsQuery(temp);
  console.log(data);
  if (isUninitialized || isLoading) {
    return <Spinner />;
  }

  const test = <ConnectionGridItem data={data!.items[0]} />;
  const gridItems = [test, test, test, test, test];
  // const gridItems = data!.items.map((d) => (
  //   <ConnectionGridItem key={d.key} data={d} />
  // ));
  return <Grid templateColumns="repeat(3, 1fr)">{gridItems}</Grid>;
};

export default ConnectionGrid;
