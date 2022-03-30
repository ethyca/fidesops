import React, { useEffect, useRef, useState } from 'react';
import {
  Table,
  Text,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Button,
  Flex,
  ButtonGroup,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Portal,
  Alert,
  AlertTitle,
  useClipboard,
  useToast,
} from '@fidesui/react';
import { format } from 'date-fns-tz';
import { useSelector } from 'react-redux';

import debounce from 'lodash.debounce';
import { MoreIcon } from '../common/Icon';
import RequestBadge from './RequestBadge';

import { PrivacyRequest } from './types';
import { useObscuredPII } from './helpers';
import {
  selectPrivacyRequestFilters,
  useGetAllPrivacyRequestsQuery,
} from './privacy-requests.slice';

interface RequestTableProps {
  requests?: PrivacyRequest[];
}

const PII: React.FC<{ data: string }> = ({ data }) => (
  <>{useObscuredPII(data)}</>
);

const useRequestRow = (request: PrivacyRequest) => {
  const toast = useToast();
  const [hovered, setHovered] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const handleMenuOpen = () => setMenuOpen(true);
  const handleMenuClose = () => setMenuOpen(false);
  const handleMouseEnter = () => setHovered(true);
  const handleMouseLeave = () => setHovered(false);
  const { onCopy } = useClipboard(request.id);
  const handleIdCopy = () => {
    onCopy();
    if (typeof window !== 'undefined') {
      toast({
        title: 'Request ID copied',
        duration: 5000,
        render: () => (
          <Alert bg="gray.600" borderRadius="6px" display="flex">
            <AlertTitle color="white">Request ID copied</AlertTitle>
          </Alert>
        ),
        containerStyle: {
          minWidth: '0px',
        },
      });
    }
  };
  return {
    hovered,
    handleMenuClose,
    handleMenuOpen,
    handleMouseEnter,
    handleMouseLeave,
    handleIdCopy,
    menuOpen,
  };
};

const RequestRow: React.FC<{ request: PrivacyRequest }> = ({ request }) => {
  const {
    hovered,
    handleMenuOpen,
    handleMenuClose,
    handleMouseEnter,
    handleMouseLeave,
    handleIdCopy,
    menuOpen,
  } = useRequestRow(request);
  return (
    <Tr
      key={request.id}
      _hover={{ bg: 'gray.50' }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      height="36px"
    >
      <Td pl={0} py={1}>
        <RequestBadge status={request.status} />
      </Td>
      <Td py={1} />
      <Td py={1}>
        <Text fontSize="xs">
          <PII
            data={
              request.identity
                ? request.identity.email || request.identity.phone || ''
                : ''
            }
          />
        </Text>
      </Td>
      <Td py={1}>
        <Text fontSize="xs">
          {format(new Date(request.created_at), 'MMMM d, Y, KK:mm:ss z')}
        </Text>
      </Td>
      <Td py={1}>
        <Text fontSize="xs">
          <PII data={request.reviewed_by || ''} />
        </Text>
      </Td>
      <Td py={1}>
        <Text isTruncated fontSize="xs" maxWidth="87px">
          {request.id}
        </Text>
      </Td>
      <Td pr={0} py={1} textAlign="end" position="relative">
        <Button size="xs" variant="ghost" mr={2.5}>
          <MoreIcon color="gray.700" w={18} h={18} />
        </Button>
        {hovered || menuOpen ? (
          <ButtonGroup
            isAttached
            variant="outline"
            position="absolute"
            right={2.5}
            top="50%"
            transform="translate(1px, -50%)"
          >
            <Button size="xs" mr="-px" bg="white">
              Approve
            </Button>
            <Button size="xs" mr="-px" bg="white">
              Deny
            </Button>
            <Menu onOpen={handleMenuOpen} onClose={handleMenuClose}>
              <MenuButton as={Button} size="xs" bg="white">
                <MoreIcon color="gray.700" w={18} h={18} />
              </MenuButton>
              <Portal>
                <MenuList>
                  <MenuItem
                    _focus={{ color: 'complimentary.500', bg: 'gray.100' }}
                    onClick={handleIdCopy}
                  >
                    <Text fontSize="sm">Copy Request ID</Text>
                  </MenuItem>
                </MenuList>
              </Portal>
            </Menu>
          </ButtonGroup>
        ) : null}
      </Td>
    </Tr>
  );
};

const useRequestTable = () => {
  const filters = useSelector(selectPrivacyRequestFilters);
  const [cachedFilters, setCachedFilters] = useState(filters);
  const updateCachedFilters = useRef(
    debounce((updatedFilters) => setCachedFilters(updatedFilters), 250)
  );
  useEffect(() => {
    updateCachedFilters.current(filters);
  }, [setCachedFilters, filters]);
  const { data: requests = [] } = useGetAllPrivacyRequestsQuery(cachedFilters);
  return { requests };
};

const RequestTable: React.FC<RequestTableProps> = () => {
  const { requests } = useRequestTable();
  return (
    <>
      <Table size="sm">
        <Thead>
          <Tr>
            <Th pl={0}>Status</Th>
            <Th>Policy Name</Th>
            <Th>Subject Identity</Th>
            <Th>Time Received</Th>
            <Th>Reviewed By</Th>
            <Th>Request ID</Th>
            <Th />
          </Tr>
        </Thead>
        <Tbody>
          {requests.map((request) => (
            <RequestRow request={request} key={request.id} />
          ))}
        </Tbody>
      </Table>
      <Flex justifyContent="space-between" mt={6}>
        <Text fontSize="xs" color="gray.600">
          {requests ? requests.length : 0} results
        </Text>
        <div>
          <Button disabled mr={2} size="sm">
            Previous
          </Button>
          <Button disabled size="sm">
            Next
          </Button>
        </div>
      </Flex>
    </>
  );
};

RequestTable.defaultProps = {
  requests: [],
};

export default RequestTable;
