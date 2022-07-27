import { ArrowBackIcon } from "@chakra-ui/icons";
import { Button, useDisclosure } from "@chakra-ui/react";
import { FocusableElement } from "@chakra-ui/utils";
import {
  Box,
  Divider,
  Drawer,
  DrawerBody,
  DrawerContent,
  DrawerHeader,
  DrawerOverlay,
  Flex,
  IconButton,
  Text,
} from "@fidesui/react";
import { CloseSolidIcon } from "common/Icon";
import React, { LegacyRef, RefObject, useRef, useState } from "react";

import { ExecutionLog } from "../../privacy-requests/types";
import EventError from "./EventError";
import EventLog from "./EventLog";

export type EventData = {
  key: string;
  logs: ExecutionLog[];
};

type EventDetailsProps = {
  eventData: EventData | undefined;
};

const EventDetails = ({ eventData }: EventDetailsProps) => {
  const { isOpen, onOpen, onClose } = useDisclosure();

  const [isViewingError, setViewingError] = useState(false);

  const toggleIsViewingError = () => {
    setViewingError(!isViewingError);
  };
  const closeDrawer = () => {
    if (isViewingError) {
      toggleIsViewingError();
    }

    onClose();
  };
  const btnRef = useRef<unknown>();

  const headerText = isViewingError ? "Event detail" : "Event log";
  if (eventData === undefined) {
    return null;
  }
  return (
    <Box width="100%" paddingTop="0px" height="100%">
      <Text color="gray.900" fontSize="md" fontWeight="500" mb={1}>
        Event Details
      </Text>

      <Text
        color="gray.600"
        fontSize="sm"
        fontWeight="500"
        lineHeight="20px"
        mb={1}
      >
        {eventData.key}
      </Text>
      <Divider />

      <Text
        cursor="pointer"
        color="complimentary.500"
        fontWeight="500"
        fontSize="sm"
        onClick={() => {
          onOpen();
        }}
      >
        View Log
      </Text>

      {/* <Button */}
      {/*   ref={btnRef as LegacyRef<HTMLButtonElement> | undefined} */}
      {/*   colorScheme="teal" */}
      {/*   onClick={() => { */}
      {/*     onOpen(); */}
      {/*   }} */}
      {/* > */}
      {/*   Open */}
      {/* </Button> */}
      <Drawer
        isOpen={isOpen}
        placement="right"
        onClose={onClose}
        size="full"
        finalFocusRef={btnRef as RefObject<FocusableElement>}
      >
        <DrawerOverlay />
        <DrawerContent style={{ width: "50%" }}>
          <DrawerHeader
            style={{
              paddingBottom: "0px",
            }}
          >
            <Flex
              justifyContent="space-between"
              alignItems="center"
              height="40px"
            >
              <Flex alignItems="center">
                {isViewingError ? (
                  <IconButton
                    icon={<ArrowBackIcon />}
                    aria-label="Close Event Logs"
                    size="sm"
                    style={{
                      height: "24px",
                      width: "24px",
                      minWidth: "24px",
                      marginRight: "8px",
                    }}
                    onClick={closeDrawer}
                  />
                ) : null}
                <Text
                  color="gray.900"
                  fontSize="md"
                  lineHeight="6"
                  fontWeight="medium"
                >
                  {headerText}
                </Text>
              </Flex>

              <Flex alignItems="flex-start" height="100%">
                <IconButton
                  icon={<CloseSolidIcon />}
                  aria-label="Stop viewing error message"
                  variant="unstyled"
                  size="sm"
                  style={{
                    height: "24px",
                    width: "24px",
                    minWidth: "14px",
                    backgroundColor: "#00000000",
                  }}
                  isRound
                  onClick={() => {
                    toggleIsViewingError();
                  }}
                />
              </Flex>
            </Flex>
          </DrawerHeader>
          <DrawerBody id="drawerBody" overflow="hidden">
            {eventData && !isViewingError ? (
              <EventLog
                eventLogs={eventData.logs}
                openStackTrace={toggleIsViewingError}
              />
            ) : null}
            {isViewingError ? <EventError errorMessage="stacktrace!" /> : null}
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </Box>
  );
};

export default EventDetails;
