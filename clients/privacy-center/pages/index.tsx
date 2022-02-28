import React from 'react';
import type { NextPage } from 'next';
import Head from 'next/head';
import { Session } from 'next-auth';
import { Flex, Heading, Text, Stack, Box, Grid, theme } from '@fidesui/react';
import Image from 'next/image';

import config from '../fides-config.json';

const Home: NextPage<{ session: Session }> = () => (
  <div>
    <Head>
      <title>FidesUI App</title>
      <meta name="description" content="Generated from FidesUI template" />
      <link rel="icon" href="/favicon.ico" />
    </Head>

    <header>
      <Flex
        bg="gray.100"
        height={16}
        width="100%"
        justifyContent="center"
        alignItems="center"
      >
        <Flex
          height="56px"
          width={[142, 304]}
          bg="gray.50"
          alignItems="center"
          justifyContent="center"
          border="1px dashed #A0AEC0"
        />
      </Flex>
    </header>
    <main>
      <Stack align="center" py={['6', '16']} px={5} spacing={8}>
        <Stack align="center" spacing={3}>
          <Heading
            fontSize={['3xl', '4xl']}
            color="gray.600"
            textAlign="center"
          >
            {config.heading}
          </Heading>
          <Text
            fontSize={['sm', 'md']}
            fontWeight="medium"
            maxWidth={624}
            textAlign="center"
            color="gray.600"
          >
            {config.description}
          </Text>
        </Stack>
        <Grid
          templateColumns={[
            'repeat(1, 1fr)',
            'repeat(1, 1fr)',
            'repeat(3, 1fr)',
          ]}
          gap={4}
        >
          {config.actions.map((action) => (
            <Box
              key={action.title}
              bg="white"
              py={8}
              px={6}
              borderRadius={4}
              boxShadow="base"
              maxWidth={['100%', '100%', '100%', 304]}
              transition="box-shadow 50ms"
              cursor="pointer"
              userSelect="none"
              _hover={{
                boxShadow: 'complimentary-2xl',
              }}
            >
              <Stack spacing={7}>
                <Flex width="100%" justifyContent="center">
                  <Image
                    src={`/${action.icon}`}
                    alt={action.description}
                    width={54}
                    height={54}
                  />
                </Flex>
                <Stack spacing={1} textAlign="center">
                  <Heading fontSize="large" lineHeight="28px" color="gray.600">
                    {action.title}
                  </Heading>
                  <Text fontSize="xs" color="gray.600">
                    {action.description}
                  </Text>
                </Stack>
              </Stack>
            </Box>
          ))}
        </Grid>
      </Stack>
    </main>
  </div>
);

export default Home;
