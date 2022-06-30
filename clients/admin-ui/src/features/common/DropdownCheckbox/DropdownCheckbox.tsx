import { PlacementWithLogical } from "@chakra-ui/react";
import { Button, Grid, Menu, MenuButton, Text, Tooltip } from "@fidesui/react";
import React, { useEffect, useRef, useState } from "react";
import { ArrowDownLineIcon } from "../Icon";
import DropdownCheckboxList from "./DropdownCheckboxList";

interface Props {
  list: Map<string, boolean>;
  title: string;
  closeOnSelect?: boolean;
  minWidth?: string;
  onChange: (values: string[]) => void;
  tooltipPlacement?: PlacementWithLogical;
}

const DropdownCheckbox: React.FC<Props> = (props) => {
  // Clone default checklist
  const defaultItems = new Map(props.list);

  // Hooks
  const [isOpen, setIsOpen] = useState(false);
  const [selectedItems, setSelectedItems] = useState(
    new Map<string, boolean>()
  );
  const didMount = useRef(false);
  useEffect(() => {
    // Only execute the following if the component is mounted
    if (didMount.current) {
      props.onChange([...selectedItems.keys()]);
    } else {
      didMount.current = true;
    }
  }, [selectedItems]);

  // Listeners
  const changeHandler = (items: Map<string, boolean>) => {
    // Filter out the selected items
    let temp = new Map<string, boolean>();
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
      : props.title;

  return (
    <Grid>
      <Menu
        closeOnSelect={props.closeOnSelect}
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
          isDisabled={selectedItems.size > 0 ? false : true}
          placement={props.tooltipPlacement}
        >
          <MenuButton
            aria-label={props.title}
            as={Button}
            fontWeight="normal"
            minWidth={props.minWidth}
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
            <Text isTruncated={true}>{selectedItemsText}</Text>
          </MenuButton>
        </Tooltip>
        {isOpen ? (
          <DropdownCheckboxList
            defaultValues={[...selectedItems.keys()]}
            items={defaultItems}
            minWidth={props.minWidth}
            onSelection={selectionHandler}
          />
        ) : null}
      </Menu>
    </Grid>
  );
};

export default DropdownCheckbox;
