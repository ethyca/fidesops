import { PlacementWithLogical } from "@chakra-ui/react";
import { Button, Grid, Menu, MenuButton, Text, Tooltip } from "@fidesui/react";
import React, { useEffect, useRef, useState } from "react";

import { ArrowDownLineIcon } from "../Icon";
import DropdownCheckboxList from "./DropdownCheckboxList";

export type DropdownCheckboxProps = {
  /**
   * List of key/value pairs to be rendered as a checkbox list
   */
  list: Map<string, boolean>;
  /**
   * Placeholder
   */
  title: string;
  /**
   * Boolean to determine if the dropdown is to be immediately close on a user selection
   */
  closeOnSelect?: boolean;
  /**
   * Minimum width of an element
   */
  minWidth?: string;
  /**
   * Event handler invoked when list of selection values have changed
   */
  onChange: (values: string[]) => void;
  /**
   * Position of the tooltip
   */
  tooltipPlacement?: PlacementWithLogical;
};

const DropdownCheckbox: React.FC<DropdownCheckboxProps> = ({
  closeOnSelect,
  list,
  minWidth,
  onChange,
  title,
  tooltipPlacement,
}) => {
  const defaultItems = new Map(list);

  // Hooks
  const [isOpen, setIsOpen] = useState(false);
  const [selectedItems, setSelectedItems] = useState(
    new Map<string, boolean>()
  );
  const didMount = useRef(false);
  useEffect(() => {
    // Only execute the following if the component is mounted
    if (didMount.current) {
      onChange([...selectedItems.keys()]);
    } else {
      didMount.current = true;
    }
  }, [onChange, selectedItems]);

  // Listeners
  const changeHandler = (items: Map<string, boolean>) => {
    // Filter out the selected items
    const temp = new Map<string, boolean>();
    items.forEach((value, key) => {
      if (value) {
        temp.set(key, value);
      }
    });
    setSelectedItems(temp);
  };
  const selectionHandler = (items: Map<string, boolean>) => {
    setIsOpen(false);
    changeHandler(items);
  };
  const openHandler = () => {
    setIsOpen(true);
  };
  const selectedItemsText =
    selectedItems.size > 0
      ? [...selectedItems.keys()].sort().join(", ")
      : title;

  return (
    <Grid>
      <Menu
        closeOnSelect={closeOnSelect}
        isLazy
        onClose={() => setIsOpen(false)}
        onOpen={openHandler}
      >
        <Tooltip
          fontSize=".75rem"
          hasArrow
          aria-label=""
          label={selectedItemsText}
          lineHeight="1.25rem"
          isDisabled={!(selectedItems.size > 0)}
          placement={tooltipPlacement}
        >
          <MenuButton
            aria-label={title}
            as={Button}
            fontWeight="normal"
            minWidth={minWidth}
            rightIcon={<ArrowDownLineIcon />}
            size="sm"
            variant="outline"
            _active={{
              bg: "none",
            }}
            _hover={{
              bg: "none",
            }}
          >
            <Text isTruncated>{selectedItemsText}</Text>
          </MenuButton>
        </Tooltip>
        {isOpen ? (
          <DropdownCheckboxList
            defaultValues={[...selectedItems.keys()]}
            items={defaultItems}
            minWidth={minWidth}
            onSelection={selectionHandler}
          />
        ) : null}
      </Menu>
    </Grid>
  );
};

export default DropdownCheckbox;
