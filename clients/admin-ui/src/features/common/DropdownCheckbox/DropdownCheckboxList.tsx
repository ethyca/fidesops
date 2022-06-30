import {
  Button,
  Checkbox,
  CheckboxGroup,
  Flex,
  MenuItem,
  MenuList,
  Spacer,
  Text,
} from "@fidesui/react";
import React, { useState } from "react";

interface Props {
  defaultValues?: string[]; // List of default item values
  items: Map<string, boolean>; // List of key/value pair items
  minWidth?: string;
  onSelection: (items: Map<string, boolean>) => void;
}

const DropdownCheckboxList: React.FC<Props> = (props) => {
  const [pendingItems, setPendingItems] = useState(props.items);

  // Listeners
  const changeHandler = (values: string[]) => {
    // Copy items
    let temp = new Map(pendingItems);

    // Uncheck all items
    temp.forEach((value, key) => {
      temp.set(key, false);
    });

    // Check the selected items
    values.forEach((v) => {
      temp.set(v, true);
    });

    setPendingItems(temp);
  };
  const clearHandler = () => {
    setPendingItems(props.items);
    props.onSelection(new Map<string, boolean>());
  };
  const doneHandler = () => {
    props.onSelection(pendingItems);
  };
  return (
    <MenuList lineHeight="1rem" minWidth={props.minWidth} p="0">
      <Flex
        borderBottom="1px"
        borderColor="gray.200"
        cursor="auto"
        p="8px"
        _focus={{
          bg: "none",
        }}
      >
        <Button onClick={clearHandler} size="xs" variant="outline">
          Clear
        </Button>
        <Spacer />
        <Button
          onClick={doneHandler}
          size="xs"
          backgroundColor="primary.800"
          color="white"
        >
          Done
        </Button>
      </Flex>
      {/* MenuItems are not rendered unless Menu is open */}
      <CheckboxGroup
        colorScheme="purple"
        defaultValue={props.defaultValues}
        onChange={changeHandler}
      >
        {[...props.items].sort().map(([key]) => (
          <MenuItem
            key={key}
            paddingTop="10px"
            paddingRight="8.5px"
            paddingBottom="10px"
            paddingLeft="8.5px"
            _focus={{
              bg: "gray.100",
            }}
          >
            <Checkbox
              aria-label={key}
              isChecked={props.items.get(key)}
              spacing=".5rem"
              value={key}
              width="100%"
            >
              <Text fontSize="0.75rem">{key}</Text>
            </Checkbox>
          </MenuItem>
        ))}
      </CheckboxGroup>
    </MenuList>
  );
};

export default DropdownCheckboxList;
