import {
  Box,
  Table,
  TableContainer,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
  Tr,
} from "@fidesui/react";
import { format } from "date-fns-tz";
import React from "react";

import { ExecutionLog, ExecutionLogStatus } from "../privacy-requests/types";

type EventDetailsProps = {
  eventDetails: ExecutionLog[];
  openStackTrace: () => void;
};

const EventDetails = ({ eventDetails, openStackTrace }: EventDetailsProps) => {
  const isError = "sdfsdfsdf";
  const tableItems = eventDetails?.map((detail) => (
    <Tr
      key={detail.updated_at}
      _hover={{
        backgroundColor: "#F7FAFC",
      }}
      onClick={() => {
        if (detail.status === ExecutionLogStatus.IN_PROCESSING) {
          openStackTrace();
        }
      }}
      style={{
        cursor:
          detail.status === ExecutionLogStatus.IN_PROCESSING
            ? "pointer"
            : "unset",
      }}
    >
      <Td>
        <Text color="gray.600" fontSize="xs" lineHeight="4" fontWeight="medium">
          {format(new Date(detail.updated_at), "MMMM d, Y, KK:mm:ss z")}
        </Text>
      </Td>
      <Td>
        <Text color="gray.600" fontSize="xs" lineHeight="4" fontWeight="medium">
          {detail.status}
        </Text>
      </Td>
      <Td>
        <Text color="gray.600" fontSize="xs" lineHeight="4" fontWeight="medium">
          {detail.collection_name}
        </Text>
      </Td>

      <Td>
        <Text color="gray.600" fontSize="xs" lineHeight="4" fontWeight="medium">
          {detail.message}
        </Text>
      </Td>
    </Tr>
  ));
  return (
    <Box width="100%" paddingTop="0px">
      <TableContainer
        height="600px"
        id="tableContainer"
        style={{
          overflowY: "auto",
        }}
      >
        <Table size="sm" id="table" position="relative">
          <Thead
            id="tableHeader"
            position="sticky"
            top="0px"
            backgroundColor="white"
          >
            <Tr>
              <Th>
                <Text
                  color="black"
                  fontSize="xs"
                  lineHeight="4"
                  fontWeight="medium"
                >
                  Time
                </Text>
              </Th>
              <Th>
                <Text
                  color="black"
                  fontSize="xs"
                  lineHeight="4"
                  fontWeight="medium"
                >
                  Status
                </Text>
              </Th>
              <Th>
                <Text
                  color="black"
                  fontSize="xs"
                  lineHeight="4"
                  fontWeight="medium"
                >
                  Collection
                </Text>
              </Th>
              <Th>
                <Text
                  color="black"
                  fontSize="xs"
                  lineHeight="4"
                  fontWeight="medium"
                >
                  Event Details
                </Text>
              </Th>
            </Tr>
          </Thead>

          <Tbody id="tabelBody">
            {tableItems}
            {tableItems}
          </Tbody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default EventDetails;
