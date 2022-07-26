import { ArrowBackIcon } from "@chakra-ui/icons";
import { Button, useDisclosure } from "@chakra-ui/react";
import { FocusableElement } from "@chakra-ui/utils";
import {
  Divider,
  Drawer,
  DrawerBody,
  DrawerContent,
  DrawerHeader,
  DrawerOverlay,
  Flex,
  Heading,
  IconButton,
  Text,
} from "@fidesui/react";
import { CloseSolidIcon } from "common/Icon";
import React, { LegacyRef, RefObject, useRef, useState } from "react";

import { ExecutionLog, PrivacyRequest } from "../privacy-requests/types";
import ActivityTimeline from "./ActivityTimeline";
import EventDetails from "./EventDetails";
import EventError from "./EventError";

type EventsAndLogsProps = {
  subjectRequest: PrivacyRequest;
};

const EventsAndLogs = ({ subjectRequest }: EventsAndLogsProps) => {
  const [eventDetails, setEventDetails] = useState<null | ExecutionLog[]>(null);
  const [isViewingError, setViewingError] = useState(false);

  const toggleIsViewingError = () => {
    setViewingError(!isViewingError);
  };
  const { isOpen, onOpen, onClose } = useDisclosure();

  const closeDrawer = () => {
    if (isViewingError) {
      toggleIsViewingError();
    }

    onClose();
  };

  const btnRef = useRef<unknown>();
  const headerText = isViewingError ? "Event detail" : "Event log";
  return (
    <>
      <Heading fontSize="lg" fontWeight="semibold" mb={4}>
        Events and logs
      </Heading>
      <Divider />
      <Flex mt={3}>
        <ActivityTimeline
          subjectRequest={subjectRequest}
          setEventDetails={setEventDetails}
        />
        <Button
          ref={btnRef as LegacyRef<HTMLButtonElement> | undefined}
          colorScheme="teal"
          onClick={() => {
            onOpen();
            setEventDetails(subjectRequest.results!.postgres_example);
          }}
        >
          Open
        </Button>
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
                      onClick={toggleIsViewingError}
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
              {eventDetails && !isViewingError ? (
                <EventDetails
                  eventDetails={eventDetails}
                  openStackTrace={toggleIsViewingError}
                />
              ) : null}
              {isViewingError ? (
                <EventError errorMessage="stacktrace!" />
              ) : null}
            </DrawerBody>
          </DrawerContent>
        </Drawer>
      </Flex>
    </>
  );
};

export default EventsAndLogs;
