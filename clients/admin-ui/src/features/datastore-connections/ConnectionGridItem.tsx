import { Box, Text } from '@fidesui/react';

import { DatastoreConnection } from './types';

type ConnectionGridItemProps = {
  data: DatastoreConnection;
};

const ConnectionGridItem: React.FC<ConnectionGridItemProps> = ({ data }) => (
  <Box width={400} height={136} border="1px" borderColor="blackAlpha.300">
    <Text color="gray.900" fontSize="md" fontWeight="medium">
      {data.name}
    </Text>
  </Box>
);

export default ConnectionGridItem;
