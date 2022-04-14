import React from 'react';
import {Flex, Button } from '@fidesui/react';
import type { NextPage } from 'next';
import NextLink from 'next/link'

import { ArrowDownLineIcon } from '../../features/common/Icon';

import Header from './Header';

const NavBar: NextPage<{ session: { username: string } }> = ({ session }) => (
  <>
    <Header username={session.username} />
    <Flex
      borderBottom="1px"
      borderTop="1px"
      px={9}
      py={1}
      borderColor="gray.100"
    >
      <NextLink href="/" passHref>
        <Button as="a" variant="ghost" mr={4} colorScheme="complimentary">
          Subject Requests
        </Button>
      </NextLink>

      <NextLink href="#" passHref>
        <Button as="a" variant="ghost" disabled mr={4}>
          Datastore Connections
        </Button>
      </NextLink>

      <NextLink href="/user-management" passHref>
        <Button as="a" variant="ghost" mr={4} colorScheme="ghost">
          User Management
        </Button>
      </NextLink>

      <NextLink href="#" passHref>
        <Button as="a" variant="ghost" disabled rightIcon={<ArrowDownLineIcon />}>
          More
        </Button>
      </NextLink>
    </Flex>
  </>
);

export default NavBar;