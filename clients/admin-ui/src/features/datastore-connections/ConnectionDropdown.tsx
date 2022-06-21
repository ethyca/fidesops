import { Box, Flex, IconButton, Spacer, Text } from "@fidesui/react";
import React, { useState } from "react";

import { ArrowDownLineIcon } from "../common/Icon";
import { capitalize } from "../common/utils";

const useConnectionStatusMenu = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return {
    isOpen,
    toggleMenu,
  };
};

type ConnectionDropdownProps = {
  filterOptions: string[];
  // eslint-disable-next-line react/require-default-props
  value?: string;
  setValue: (x: string) => void;
  title: string;
};

const ConnectionDropdown: React.FC<ConnectionDropdownProps> = ({
  filterOptions,
  value,
  setValue,
  title,
}) => {
  const { isOpen, toggleMenu } = useConnectionStatusMenu();
  const options = filterOptions.map((d) => (
    <Flex
      key={d}
      height="36px"
      _hover={{ bg: "gray.100" }}
      alignItems="center"
      padding="8px"
      cursor="pointer"
      onClick={() => {
        console.log("setting the value to ", d);
        setValue(d);
      }}
    >
      <Text
        marginLeft="8px"
        fontSize="xs"
        fontWeight="500"
        color={d === value ? "complimentary.500" : "gray.700"}
        lineHeight="16px"
      >
        {capitalize(d)}
      </Text>
    </Flex>
  ));

  return (
    <Box width="100%" position="relative">
      <Flex
        borderRadius="6px"
        border="1px"
        borderColor={isOpen ? "primary.600" : "gray.200"}
        height="32px"
        paddingRight="14px"
        paddingLeft="14px"
        alignItems="center"
      >
        <Text
          fontSize="14px"
          fontWeight="400"
          lineHeight="20px"
          color="gray.700"
        >
          {title}
        </Text>
        <Spacer />
        <IconButton
          variant="ghost"
          size="xs"
          aria-label="Datastore Type Dropdown"
          onClick={() => toggleMenu()}
          icon={<ArrowDownLineIcon />}
        />
      </Flex>
      {isOpen ? (
        <Flex
          marginTop="4px"
          backgroundColor="white"
          flexDirection="column"
          border="1px"
          width="100%"
          borderColor="gray.200"
          boxShadow="0px 1px 3px rgba(0, 0, 0, 0.1), 0px 1px 2px rgba(0, 0, 0, 0.06);"
          borderRadius="4px"
          position="absolute"
          zIndex={1}
        >
          {options}
        </Flex>
      ) : null}
    </Box>
  );
};

export default ConnectionDropdown;
