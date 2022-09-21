import {
  Box,
  Button,
  Center,
  Divider,
  Heading,
  Spinner,
  Table,
  TableContainer,
  Tbody,
  Td,
  Text,
  Tfoot,
  Th,
  Thead,
  Tr,
  VStack,
} from "@fidesui/react";
import { useGetAllEnabledAccessManualHooksQuery } from "datastore-connections/datastore-connection.slice";
import { privacyRequestApi } from "privacy-requests/privacy-requests.slice";
import { PrivacyRequest } from "privacy-requests/types";
import React, { useCallback, useEffect, useRef, useState } from "react";
import { useDispatch } from "react-redux";

import ManualProcessingDetail from "./ManualProcessingDetail";
import { ManualInputData } from "./types";

type ManualProcessingListProps = {
  subjectRequest: PrivacyRequest;
};

const ManualProcessingList: React.FC<ManualProcessingListProps> = ({
  subjectRequest,
}) => {
  const dispatch = useDispatch();
  const mounted = useRef(false);
  const [dataList, setDataList] = useState([] as unknown as ManualInputData[]);

  const { data, isFetching, isLoading, isSuccess } =
    useGetAllEnabledAccessManualHooksQuery();

  const fetchUploadedManuaWebhookData = useCallback(() => {
    const promises: any[] = [];
    const keys = data?.map((item) => item.connection_config.key);
    keys?.every((k) =>
      promises.push(
        dispatch(
          privacyRequestApi.endpoints.getUploadedManualWebhookData.initiate({
            connection_key: k,
            privacy_request_id: subjectRequest.id,
          })
        )
      )
    );
    Promise.allSettled(promises).then((results) => {
      const list: ManualInputData[] = [];
      results.forEach((result) => {
        if (
          result.status === "fulfilled" &&
          result.value.isSuccess &&
          result.value.data
        ) {
          const item = {
            checked: result.value.data.checked,
            fields: [],
            key: result.value.originalArgs.connection_key,
          } as ManualInputData;
          Object.entries(result.value.data.fields).forEach(([key, value]) => {
            // @ts-ignore
            item.fields[key] = value || "";
          });
          list.push(item);
        }
      });
      setDataList(list);
    });
  }, [data, dispatch, subjectRequest.id]);

  useEffect(() => {
    mounted.current = true;
    if (isSuccess && data!.length > 0) {
      fetchUploadedManuaWebhookData();
    }
    return () => {
      mounted.current = false;
    };
  }, [fetchUploadedManuaWebhookData, data, isSuccess]);

  return (
    <VStack align="stretch" spacing={8}>
      <Box>
        <Heading color="gray.900" fontSize="lg" fontWeight="semibold" mb={4}>
          Manual Processing
        </Heading>
        <Divider />
      </Box>
      <Box>
        <Text color="gray.700" fontSize="sm">
          The following table details the integrations that require manual input
          from you.
        </Text>
      </Box>
      <Box>
        {(isFetching || isLoading) && (
          <Center>
            <Spinner />
          </Center>
        )}
        {isSuccess && data ? (
          <TableContainer>
            <Table size="sm" variant="unstyled">
              <Thead>
                <Tr>
                  <Th
                    fontSize="sm"
                    fontWeight="semibold"
                    pl="0"
                    textTransform="none"
                  >
                    Connector name
                  </Th>
                  <Th fontSize="sm" fontWeight="semibold" textTransform="none">
                    Description
                  </Th>
                  <Th />
                </Tr>
              </Thead>
              <Tbody>
                {data.length > 0 &&
                  data.map((item) => (
                    <Tr key={item.id}>
                      <Td pl="0">{item.connection_config.name}</Td>
                      <Td>{item.connection_config.description}</Td>
                      <Td>
                        {dataList.length > 0 ? (
                          <ManualProcessingDetail
                            connectorName={item.connection_config.name}
                            data={
                              dataList.find(
                                (i) => i.key === item.connection_config.key
                              ) as ManualInputData
                            }
                          />
                        ) : null}
                      </Td>
                    </Tr>
                  ))}
                {data.length === 0 && (
                  <Tr>
                    <Td colSpan={3} pl="0">
                      <Center>
                        <Text>
                          You don&lsquo;t have any Manual Webhook connections
                          set up yet.
                        </Text>
                      </Center>
                    </Td>
                  </Tr>
                )}
              </Tbody>
              {dataList.length > 0 && dataList.every((item) => item.checked) ? (
                <Tfoot>
                  <Tr>
                    <Th />
                    <Th />
                    <Th>
                      <Button
                        color="white"
                        bg="primary.800"
                        fontSize="xs"
                        h="24px"
                        w="127px"
                        _hover={{ bg: "primary.400" }}
                        _active={{ bg: "primary.500" }}
                      >
                        Complete DSR
                      </Button>
                    </Th>
                  </Tr>
                </Tfoot>
              ) : null}
            </Table>
          </TableContainer>
        ) : null}
      </Box>
    </VStack>
  );
};

export default ManualProcessingList;
