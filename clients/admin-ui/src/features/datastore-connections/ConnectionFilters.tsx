import {
  Input,
  InputGroup,
  InputLeftElement,
  Select,
  Stack,
  useToast,
} from "@fidesui/react";
import React from "react";
import { useDispatch, useSelector } from "react-redux";

import { selectToken } from "../auth";
import { SearchLineIcon } from "../common/Icon";
import { statusPropMap } from "../common/RequestStatusBadge";
import {
  clearAllFilters,
  requestCSVDownload,
  selectPrivacyRequestFilters,
  setRequestFrom,
  setRequestId,
  setRequestStatus,
  setRequestTo,
} from "../privacy-requests";
import { PrivacyRequestStatus } from "../privacy-requests/types";

const useConstantFilters = () => {
  const filters = useSelector(selectPrivacyRequestFilters);
  const token = useSelector(selectToken);
  const dispatch = useDispatch();
  const toast = useToast();
  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) =>
    dispatch(setRequestId(event.target.value));
  const handleStatusChange = (event: React.ChangeEvent<HTMLSelectElement>) =>
    dispatch(setRequestStatus(event.target.value as PrivacyRequestStatus));
  const handleFromChange = (event: React.ChangeEvent<HTMLInputElement>) =>
    dispatch(setRequestFrom(event?.target.value));
  const handleToChange = (event: React.ChangeEvent<HTMLInputElement>) =>
    dispatch(setRequestTo(event?.target.value));
  const handleClearAllFilters = () => dispatch(clearAllFilters());
  const handleDownloadClick = async () => {
    let message;
    try {
      await requestCSVDownload({ ...filters, token });
    } catch (error) {
      if (error instanceof Error) {
        message = error.message;
      } else {
        message = "Unknown error occurred";
      }
    }
    if (message) {
      toast({
        description: `${message}`,
        duration: 5000,
        status: "error",
      });
    }
  };

  return {
    handleSearchChange,
    handleStatusChange,
    handleFromChange,
    handleToChange,
    handleClearAllFilters,
    handleDownloadClick,
    ...filters,
  };
};

const StatusOption: React.FC<{ status: PrivacyRequestStatus }> = ({
  status,
}) => <option value={status}>{statusPropMap[status].label}</option>;

const ConnectionFilters: React.FC = () => {
  const { status, handleSearchChange, handleStatusChange, id } =
    useConstantFilters();
  return (
    <Stack direction="row" spacing={4} mb={6}>
      <InputGroup size="sm">
        <InputLeftElement pointerEvents="none">
          <SearchLineIcon color="gray.300" w="17px" h="17px" />
        </InputLeftElement>
        <Input
          type="search"
          minWidth={200}
          placeholder="Search"
          size="sm"
          borderRadius="md"
          value={id}
          name="search"
          onChange={handleSearchChange}
        />
      </InputGroup>
      <Select
        placeholder="Datastore Type"
        size="sm"
        minWidth="144px"
        value={status || ""}
        onChange={handleStatusChange}
        borderRadius="md"
      >
        <StatusOption status="approved" />
        <StatusOption status="complete" />
        <StatusOption status="denied" />
        <StatusOption status="error" />
        <StatusOption status="in_processing" />
        <StatusOption status="paused" />
        <StatusOption status="pending" />
      </Select>
      <Select
        placeholder="System Type"
        size="sm"
        minWidth="144px"
        value={status || ""}
        onChange={handleStatusChange}
        borderRadius="md"
      >
        <StatusOption status="approved" />
        <StatusOption status="complete" />
        <StatusOption status="denied" />
        <StatusOption status="error" />
        <StatusOption status="in_processing" />
        <StatusOption status="paused" />
        <StatusOption status="pending" />
      </Select>
      <Select
        placeholder="Data Category"
        size="sm"
        minWidth="144px"
        value={status || ""}
        onChange={handleStatusChange}
        borderRadius="md"
      >
        <StatusOption status="approved" />
        <StatusOption status="complete" />
        <StatusOption status="denied" />
        <StatusOption status="error" />
        <StatusOption status="in_processing" />
        <StatusOption status="paused" />
        <StatusOption status="pending" />
      </Select>
      <Select
        placeholder="Testing Status"
        size="sm"
        minWidth="144px"
        value={status || ""}
        onChange={handleStatusChange}
        borderRadius="md"
      >
        <StatusOption status="approved" />
        <StatusOption status="complete" />
        <StatusOption status="denied" />
        <StatusOption status="error" />
        <StatusOption status="in_processing" />
        <StatusOption status="paused" />
        <StatusOption status="pending" />
      </Select>
      <Select
        placeholder="Status"
        size="sm"
        minWidth="144px"
        value={status || ""}
        onChange={handleStatusChange}
        borderRadius="md"
      >
        <StatusOption status="approved" />
        <StatusOption status="complete" />
        <StatusOption status="denied" />
        <StatusOption status="error" />
        <StatusOption status="in_processing" />
        <StatusOption status="paused" />
        <StatusOption status="pending" />
      </Select>
    </Stack>
  );
};

export default ConnectionFilters;
