import { Flex, Link } from '@fidesui/react';

import NextLink from 'next/link';
import Image from 'next/image';

import { UserIcon, GearIcon } from './Icon';

const Header = () => (
  <header>
    <Flex
      bg="gray.50"
      width="100%"
      py={3}
      px={10}
      justifyContent="space-between"
      alignItems="center"
    >
      <NextLink href="/" passHref>
        {/* eslint-disable-next-line jsx-a11y/anchor-is-valid */}
        <Link display="flex">
          <Image src="/logo.svg" width={83} height={26} alt="FidesOps Logo" />
        </Link>
      </NextLink>
      <Flex alignItems="center">
        <GearIcon color="gray.700" mr={5} />
        <UserIcon color="gray.700" />
      </Flex>
    </Flex>
  </header>
);

export default Header;
