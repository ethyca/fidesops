import { Box, Divider, Flex, Heading, Text } from '@fidesui/react';
import React, { useState } from 'react';

import { ExecutionLog, PrivacyRequest } from '../privacy-requests/types';

type EventsAndLogsProps = {
  subjectRequest: PrivacyRequest;
};

const EventsAndLogs = ({ subjectRequest }: EventsAndLogsProps) => {
  const { results } = subjectRequest;

  const [eventDetails, setEventDetails] = useState<null | ExecutionLog[]>(null);
  const resultKeys = Object.keys(results!);

  const timelineEntries = resultKeys.map((key) => (
    <Box key={key}>
      <Text color='gray.600' fontWeight='500' fontSize='sm'>
        {key}
      </Text>
      <Text
        cursor='pointer'
        color='complimentary.500'
        fontWeight='500'
        fontSize='sm'
        onClick={() => {
          setEventDetails(subjectRequest.results![key]);
        }}
      >
        View Details
      </Text>
    </Box>
  ));

  return (
    <>
      <Heading fontSize='lg' fontWeight='semibold' mb={4}>
        Events and logs
      </Heading>
      <Divider />
      <Flex>
        <Box id='ActivityTimeline' width='100%'>
          <Text color='gray.900' fontSize='md' fontWeight='500' mb={1}>
            Activity Timeline
          </Text>
          {timelineEntries}
        </Box>
        <Box id='Event Details' width='100%'>
          <Text color='gray.900' fontSize='md' fontWeight='500' mb={1}>
            Event Details
          </Text>
          <Box>
            {eventDetails?.map((detail) => (
              <Text key={detail.updated_at}>
                {detail.collection_name} {detail.status} {detail.action_type}{' '}
                {detail.message}
              </Text>
            ))}
          </Box>
        </Box>
      </Flex>
    </>
  );
};

export default EventsAndLogs;
