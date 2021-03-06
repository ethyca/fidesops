import { Button, Flex } from "@fidesui/react";
import NextLink from "next/link";
import { useRouter } from "next/router";
import React from "react";

import {
  DATASTORE_CONNECTION_ROUTE,
  INDEX_ROUTE,
  USER_MANAGEMENT_ROUTE,
} from "../../constants";
import Header from "./Header";
import { ArrowDownLineIcon } from "./Icon";

const NavBar = () => {
  const router = useRouter();

  return (
    <>
      <Header />
      <Flex
        borderBottom="1px"
        borderTop="1px"
        px={9}
        py={1}
        borderColor="gray.100"
      >
        <NextLink href={INDEX_ROUTE} passHref>
          <Button
            as="a"
            variant="ghost"
            mr={4}
            colorScheme={
              router && router.pathname === INDEX_ROUTE
                ? "complimentary"
                : "ghost"
            }
          >
            Subject Requests
          </Button>
        </NextLink>

        <NextLink href={DATASTORE_CONNECTION_ROUTE} passHref>
          <Button
            as="a"
            variant="ghost"
            mr={4}
            colorScheme={
              router && router.pathname.startsWith(DATASTORE_CONNECTION_ROUTE)
                ? "complimentary"
                : "ghost"
            }
          >
            Datastore Connections
          </Button>
        </NextLink>

        <NextLink href={USER_MANAGEMENT_ROUTE} passHref>
          <Button
            as="a"
            variant="ghost"
            mr={4}
            colorScheme={
              router && router.pathname.startsWith(USER_MANAGEMENT_ROUTE)
                ? "complimentary"
                : "ghost"
            }
          >
            User Management
          </Button>
        </NextLink>

        <NextLink href="#" passHref>
          <Button
            as="a"
            variant="ghost"
            disabled
            rightIcon={<ArrowDownLineIcon />}
          >
            More
          </Button>
        </NextLink>
      </Flex>
    </>
  );
};

export default NavBar;
