import {
  Alert,
  AlertTitle,
  Button,
  ButtonGroup,
  Menu,
  MenuButton,
  MenuItem,
  MenuList,
  Portal,
  Tag,
  Td,
  Text,
  Tr,
  useClipboard,
  useToast,
} from "@fidesui/react";
import DaysLeftTag from "common/DaysLeftTag";
import { formatDate } from "common/utils";
import { useRouter } from "next/router";
import React, { useRef, useState } from "react";

import { MoreIcon } from "../common/Icon";
import PII from "../common/PII";
import RequestStatusBadge from "../common/RequestStatusBadge";
import DenyPrivacyRequestModal from "./DenyPrivacyRequestModal";
import {
  useApproveRequestMutation,
  useDenyRequestMutation,
} from "./privacy-requests.slice";
import { PrivacyRequest } from "./types";

const useRequestRow = (request: PrivacyRequest) => {
  const toast = useToast();
  const hoverButtonRef = useRef<HTMLButtonElement>(null);
  const [hovered, setHovered] = useState(false);
  const [focused, setFocused] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [denialReason, setDenialReason] = useState("");
  const [approveRequest, approveRequestResult] = useApproveRequestMutation();
  const [denyRequest, denyRequestResult] = useDenyRequestMutation();
  const handleMenuOpen = () => setMenuOpen(true);
  const handleMenuClose = () => setMenuOpen(false);
  const handleMouseEnter = () => setHovered(true);
  const handleMouseLeave = () => setHovered(false);
  const shiftFocusToHoverMenu = () => {
    if (hoverButtonRef.current) {
      hoverButtonRef.current.focus();
    }
  };
  const handleFocus = () => setFocused(true);
  const handleBlur = () => setFocused(false);
  const handleApproveRequest = () => approveRequest(request);
  const handleDenyRequest = (reason: string) =>
    denyRequest({ id: request.id, reason });
  const { onCopy } = useClipboard(request.id);
  const handleModalOpen = () => setModalOpen(true);
  const handleModalClose = () => {
    setModalOpen(false);
    setFocused(false);
    setHovered(false);
    setMenuOpen(false);
    if (!denyRequestResult.isLoading) {
      setDenialReason("");
    }
  };
  const handleIdCopy = () => {
    onCopy();
    if (typeof window !== "undefined") {
      toast({
        title: "Request ID copied",
        duration: 5000,
        render: () => (
          <Alert bg="gray.600" borderRadius="6px" display="flex">
            <AlertTitle color="white">Request ID copied</AlertTitle>
          </Alert>
        ),
        containerStyle: {
          minWidth: "0px",
        },
      });
    }
  };

  const router = useRouter();
  const handleViewDetails = () => {
    router.push(`/subject-request/${request.id}`);
  };
  return {
    approveRequestResult,
    denyRequestResult,
    hovered,
    focused,
    menuOpen,
    modalOpen,
    handleModalOpen,
    handleModalClose,
    handleMenuClose,
    handleMenuOpen,
    handleMouseEnter,
    handleMouseLeave,
    handleFocus,
    handleBlur,
    handleIdCopy,
    handleApproveRequest,
    handleDenyRequest,
    hoverButtonRef,
    shiftFocusToHoverMenu,
    denialReason,
    setDenialReason,
    handleViewDetails,
  };
};

const RequestRow: React.FC<{ request: PrivacyRequest }> = ({ request }) => {
  const {
    hovered,
    handleMenuOpen,
    handleMenuClose,
    handleMouseEnter,
    handleMouseLeave,
    handleApproveRequest,
    handleDenyRequest,
    handleIdCopy,
    menuOpen,
    approveRequestResult,
    denyRequestResult,
    hoverButtonRef,
    modalOpen,
    handleModalClose,
    handleModalOpen,
    shiftFocusToHoverMenu,
    handleFocus,
    handleBlur,
    focused,
    denialReason,
    setDenialReason,
    handleViewDetails,
  } = useRequestRow(request);
  const showMenu = hovered || menuOpen || focused;

  return (
    <Tr
      key={request.id}
      _hover={{ bg: "gray.50" }}
      bg={showMenu ? "gray.50" : "white"}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      height="36px"
    >
      <Td pl={0} py={1}>
        <RequestStatusBadge status={request.status} />
      </Td>
      <Td py={1}>
        <DaysLeftTag daysLeft={request.days_left} includeText={false} />
      </Td>
      <Td py={1}>
        <Tag
          color="white"
          bg="primary.400"
          px={2}
          py={0.5}
          size="sm"
          fontWeight="medium"
        >
          {request.policy.name}
        </Tag>
      </Td>
      <Td py={1}>
        <Text fontSize="xs">
          <PII
            data={
              request.identity
                ? request.identity.email || request.identity.phone_number || ""
                : ""
            }
          />
        </Text>
      </Td>
      <Td py={1}>
        <Text fontSize="xs">{formatDate(request.created_at)}</Text>
      </Td>
      <Td py={1}>
        <Text fontSize="xs">
          <PII data={request.reviewer ? request.reviewer.username : ""} />
        </Text>
      </Td>
      <Td py={1}>
        <Text isTruncated fontSize="xs" maxWidth="87px">
          {request.id}
        </Text>
      </Td>
      <Td pr={0} py={1} textAlign="end" position="relative">
        <Button
          size="xs"
          variant="ghost"
          mr={2.5}
          onFocus={shiftFocusToHoverMenu}
          tabIndex={showMenu ? -1 : 0}
        >
          <MoreIcon color="gray.700" w={18} h={18} />
        </Button>
        <ButtonGroup
          isAttached
          variant="outline"
          position="absolute"
          right={2.5}
          top="50%"
          transform="translate(1px, -50%)"
          opacity={showMenu ? 1 : 0}
          pointerEvents={showMenu ? "auto" : "none"}
          onFocus={handleFocus}
          onBlur={handleBlur}
          shadow="base"
          borderRadius="md"
        >
          {request.status === "pending" ? (
            <>
              <Button
                size="xs"
                mr="-px"
                bg="white"
                onClick={handleApproveRequest}
                isLoading={approveRequestResult.isLoading}
                _loading={{
                  opacity: 1,
                  div: { opacity: 0.4 },
                }}
                _hover={{
                  bg: "gray.100",
                }}
                ref={hoverButtonRef}
              >
                Approve
              </Button>
              <Button
                size="xs"
                mr="-px"
                bg="white"
                onClick={handleModalOpen}
                _loading={{
                  opacity: 1,
                  div: { opacity: 0.4 },
                }}
                _hover={{
                  bg: "gray.100",
                }}
              >
                Deny
              </Button>
              <DenyPrivacyRequestModal
                isOpen={modalOpen}
                isLoading={denyRequestResult.isLoading}
                handleMenuClose={handleModalClose}
                handleDenyRequest={handleDenyRequest}
                denialReason={denialReason}
                onChange={(e) => {
                  setDenialReason(e.target.value);
                }}
              />
            </>
          ) : null}

          <Menu onOpen={handleMenuOpen} onClose={handleMenuClose}>
            <MenuButton
              as={Button}
              size="xs"
              bg="white"
              ref={request.status !== "pending" ? hoverButtonRef : null}
            >
              <MoreIcon color="gray.700" w={18} h={18} />
            </MenuButton>
            <Portal>
              <MenuList shadow="xl">
                <MenuItem
                  _focus={{ color: "complimentary.500", bg: "gray.100" }}
                  onClick={handleIdCopy}
                >
                  <Text fontSize="sm">Copy Request ID</Text>
                </MenuItem>
                <MenuItem
                  _focus={{ color: "complimentary.500", bg: "gray.100" }}
                  onClick={handleViewDetails}
                >
                  <Text fontSize="sm">View Details</Text>
                </MenuItem>
              </MenuList>
            </Portal>
          </Menu>
        </ButtonGroup>
      </Td>
    </Tr>
  );
};

export default RequestRow;
