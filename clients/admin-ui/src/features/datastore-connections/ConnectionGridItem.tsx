import { Box, HStack, Text } from '@fidesui/react';
import { format } from 'date-fns-tz';
import React from 'react';

import { DatastoreConnection } from './types';

type ConnectionGridItemProps = {
  data: DatastoreConnection;
};

const ConnectionGridItem: React.FC<ConnectionGridItemProps> = ({ data }) => (
  <Box
    width={400}
    height={136}
    border="1px"
    borderColor="blackAlpha.300"
    boxSizing="border-box"
    p="18px 16px 16px 16px"
  >
    <HStack mb="6px">
      <Box width="32px" height="32px" backgroundColor="aliceblue" />
      <Text
        color="gray.900"
        fontSize="md"
        fontWeight="medium"
        m="8px"
        lineHeight="24px"
      >
        {data.name}
      </Text>
    </HStack>
    <Text
      color="gray.600"
      fontSize="sm"
      fontWeight="sm"
      lineHeight="20px"
      // mb="1px"
    >
      {/* {data.connection_type} Database Connector */}
      Mailchimp Saas Connector
    </Text>
    <Text color="gray.600" fontSize="sm" fontWeight="sm" lineHeight="20px">
      Edited on {format(new Date(data.updated_at!), 'MMMM d, Y, KK:mm:ss z')}
    </Text>

    <HStack mt="8px">
      <Box
        width="12px"
        height="12px"
        borderRadius="6px"
        backgroundColor="green.500"
      />
      <Text
        color="gray.500"
        fontSize="xs"
        fontWeight="semibold"
        lineHeight="16px"
      >
        Last tested on{' '}
        {format(new Date(data.last_test_timestamp!), 'MMMM d, Y, KK:mm:ss z')}
      </Text>
    </HStack>
  </Box>
);

export default ConnectionGridItem;
