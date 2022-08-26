import { Box, Heading, List, ListItem } from "@fidesui/react";
import { useAppSelector } from "app/hooks";
import { selectConnectionTypeState } from "connection-type/connection-type.slice";
import React from "react";

import { CONNECTOR_PARAMETERS_OPTIONS } from "./constants";

type ConfigurationSettingsNavProps = {
  /**
   * Parent callback event handler invoked when a menu option has changed
   */
  onChange: (value: string) => void;
  /**
   * Default value marked for selection
   */
  selectedItem: string;
};

const ConfigurationSettingsNav: React.FC<ConfigurationSettingsNavProps> = ({
  onChange,
  selectedItem,
}) => {
  const { connectionKey } = useAppSelector(selectConnectionTypeState);
  const options = connectionKey
    ? [...CONNECTOR_PARAMETERS_OPTIONS]
    : [...CONNECTOR_PARAMETERS_OPTIONS].splice(0, 1);

  return (
    <Box w="234px">
      <Heading as="h6" color="gray.700" fontWeight="600" size="xs">
        Configuration settings
      </Heading>
      <List
        color="gray.700"
        display="flex"
        flexDirection="column"
        fontSize="sm"
        h="64px"
        mt="4px"
        w="178px"
      >
        {options.map((item) => (
          <ListItem
            color={selectedItem === item ? "complimentary.500" : undefined}
            key={item}
            onClick={() => onChange(item)}
            p="10px 12px 10px 12px"
            userSelect="none"
            _hover={{ bg: "gray.100", cursor: "pointer" }}
          >
            {item}
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default ConfigurationSettingsNav;
