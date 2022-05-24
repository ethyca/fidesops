import { Box, Divider, Flex, Heading, Text } from '@fidesui/react';
import React, { useState } from 'react';

import { GreenCheckCircle } from '../common/Icon';
import { ExecutionLog, PrivacyRequest } from '../privacy-requests/types';

type EventsAndLogsProps = {
  subjectRequest: PrivacyRequest;
};

const EventsAndLogs = ({ subjectRequest }: EventsAndLogsProps) => {
  const { results } = subjectRequest;

  const [eventDetails, setEventDetails] = useState<null | ExecutionLog[]>(null);
  // const resultKeys = Object.keys(results!);
  const resultKeys = [
    'postgres_example',
    'postgres_example',
    'postgres_example',
  ];

  const timelineEntries = resultKeys.map((key, index) => (
    <Box key={key}>
      <Flex alignItems='center' height={23} position='relative'>
        <Box zIndex={1}>
          <GreenCheckCircle />
        </Box>
        {index === resultKeys.length - 1 ? null : (
          <Box
            width='2px'
            height='63px'
            backgroundColor='gray.700'
            position='absolute'
            top='16px'
            left='6px'
            zIndex={0}
          />
        )}

        <Text color='gray.600' fontWeight='500' fontSize='sm' ml={2}>
          {key}
        </Text>
      </Flex>
      <Text
        cursor='pointer'
        color='complimentary.500'
        fontWeight='500'
        fontSize='sm'
        ml={6}
        mb={7}
        onClick={() => {
          setEventDetails(results![key]);
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
