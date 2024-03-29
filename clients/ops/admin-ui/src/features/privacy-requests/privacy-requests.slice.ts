import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { addCommonHeaders } from "common/CommonHeaders";

import type { RootState } from "../../app/store";
import { BASE_URL } from "../../constants";
import { selectToken } from "../auth";
import {
  DenyPrivacyRequest,
  GetUpdloadedManualWebhookDataRequest,
  PatchUploadManualWebhookDataRequest,
  PrivacyRequest,
  PrivacyRequestParams,
  PrivacyRequestResponse,
  PrivacyRequestStatus,
} from "./types";

// Helpers
export function mapFiltersToSearchParams({
  status,
  id,
  from,
  to,
  page,
  size,
  verbose,
  sort_direction,
  sort_field,
}: Partial<PrivacyRequestParams>): any {
  let fromISO;
  if (from) {
    fromISO = new Date(from);
    fromISO.setUTCHours(0, 0, 0);
  }

  let toISO;
  if (to) {
    toISO = new Date(to);
    toISO.setUTCHours(23, 59, 59);
  }

  return {
    include_identities: "true",
    ...(status && status.length > 0 ? { status: status.join("&status=") } : {}),
    ...(id ? { request_id: id } : {}),
    ...(fromISO ? { created_gt: fromISO.toISOString() } : {}),
    ...(toISO ? { created_lt: toISO.toISOString() } : {}),
    ...(page ? { page: `${page}` } : {}),
    ...(typeof size !== "undefined" ? { size: `${size}` } : {}),
    ...(verbose ? { verbose } : {}),
    ...(sort_direction ? { sort_direction } : {}),
    ...(sort_field ? { sort_field } : {}),
  };
}

// Subject requests API
export const privacyRequestApi = createApi({
  reducerPath: "privacyRequestApi",
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_URL,
    prepareHeaders: (headers, { getState }) => {
      const token: string | null = selectToken(getState() as RootState);
      addCommonHeaders(headers, token);
      return headers;
    },
  }),
  tagTypes: ["Request"],
  endpoints: (build) => ({
    approveRequest: build.mutation<
      PrivacyRequest,
      Partial<PrivacyRequest> & Pick<PrivacyRequest, "id">
    >({
      query: ({ id }) => ({
        url: "privacy-request/administrate/approve",
        method: "PATCH",
        body: {
          request_ids: [id],
        },
      }),
      invalidatesTags: ["Request"],
    }),
    denyRequest: build.mutation<PrivacyRequest, DenyPrivacyRequest>({
      query: ({ id, reason }) => ({
        url: "privacy-request/administrate/deny",
        method: "PATCH",
        body: {
          request_ids: [id],
          reason,
        },
      }),
      invalidatesTags: ["Request"],
    }),
    getAllPrivacyRequests: build.query<
      PrivacyRequestResponse,
      Partial<PrivacyRequestParams>
    >({
      query: (filters) => ({
        url: `privacy-request?${decodeURIComponent(
          new URLSearchParams(mapFiltersToSearchParams(filters)).toString()
        )}`,
      }),
      providesTags: () => ["Request"],
    }),
    getUploadedManualWebhookData: build.query<
      any,
      GetUpdloadedManualWebhookDataRequest
    >({
      query: (params) => ({
        url: `privacy-request/${params.privacy_request_id}/access_manual_webhook/${params.connection_key}`,
      }),
    }),
    resumePrivacyRequestFromRequiresInput: build.mutation<any, string>({
      query: (privacy_request_id) => ({
        url: `privacy-request/${privacy_request_id}/resume_from_requires_input`,
        method: "POST",
      }),
      invalidatesTags: ["Request"],
    }),
    retry: build.mutation<PrivacyRequest, Pick<PrivacyRequest, "id">>({
      query: ({ id }) => ({
        url: `privacy-request/${id}/retry`,
        method: "POST",
      }),
      invalidatesTags: ["Request"],
    }),
    uploadManualWebhookData: build.mutation<
      any,
      PatchUploadManualWebhookDataRequest
    >({
      query: (params) => ({
        url: `privacy-request/${params.privacy_request_id}/access_manual_webhook/${params.connection_key}`,
        method: "PATCH",
        body: params.body,
      }),
    }),
  }),
});

export const {
  useApproveRequestMutation,
  useDenyRequestMutation,
  useGetAllPrivacyRequestsQuery,
  useGetUploadedManualWebhookDataQuery,
  useResumePrivacyRequestFromRequiresInputMutation,
  useRetryMutation,
  useUploadManualWebhookDataMutation,
} = privacyRequestApi;

export const requestCSVDownload = async ({
  id,
  from,
  to,
  status,
  token,
}: PrivacyRequestParams & { token: string | null }) => {
  if (!token) {
    return null;
  }

  return fetch(
    `${BASE_URL}/privacy-request?${new URLSearchParams({
      ...mapFiltersToSearchParams({
        id,
        from,
        to,
        status,
      }),
      download_csv: "true",
    })}`,
    {
      headers: {
        "Access-Control-Allow-Origin": "*",
        Authorization: `Bearer ${token}`,
        "X-Fides-Source": "fidesops-admin-ui",
      },
    }
  )
    .then((response) => {
      if (!response.ok) {
        throw new Error("Got a bad response from the server");
      }
      return response.blob();
    })
    .then((data) => {
      const a = document.createElement("a");
      a.href = window.URL.createObjectURL(data);
      a.download = "privacy-requests.csv";
      a.click();
    })
    .catch((error) => Promise.reject(error));
};

// Subject requests state (filters, etc.)
interface SubjectRequestsState {
  revealPII: boolean;
  status?: PrivacyRequestStatus[];
  id: string;
  from: string;
  to: string;
  page: number;
  size: number;
  verbose?: boolean;
  sort_field?: string;
  sort_direction?: string;
}

const initialState: SubjectRequestsState = {
  revealPII: false,
  id: "",
  from: "",
  to: "",
  page: 1,
  size: 25,
};

export const subjectRequestsSlice = createSlice({
  name: "subjectRequests",
  initialState,
  reducers: {
    setRevealPII: (state, action: PayloadAction<boolean>) => ({
      ...state,
      revealPII: action.payload,
    }),
    setRequestStatus: (
      state,
      action: PayloadAction<PrivacyRequestStatus[]>
    ) => ({
      ...state,
      page: initialState.page,
      status: action.payload,
    }),
    setRequestId: (state, action: PayloadAction<string>) => ({
      ...state,
      page: initialState.page,
      id: action.payload,
    }),
    setRequestFrom: (state, action: PayloadAction<string>) => ({
      ...state,
      page: initialState.page,
      from: action.payload,
    }),
    setRequestTo: (state, action: PayloadAction<string>) => ({
      ...state,
      page: initialState.page,
      to: action.payload,
    }),
    clearAllFilters: ({ revealPII }) => ({
      ...initialState,
      revealPII,
    }),
    setPage: (state, action: PayloadAction<number>) => ({
      ...state,
      page: action.payload,
    }),
    setSize: (state, action: PayloadAction<number>) => ({
      ...state,
      page: initialState.page,
      size: action.payload,
    }),
    setVerbose: (state, action: PayloadAction<boolean>) => ({
      ...state,
      verbose: action.payload,
    }),
    setSortField: (state, action: PayloadAction<string>) => ({
      ...state,
      sort_field: action.payload,
    }),
    setSortDirection: (state, action: PayloadAction<string>) => ({
      ...state,
      sort_direction: action.payload,
    }),
    clearSortFields: (state) => ({
      ...state,
      sort_direction: undefined,
      sort_field: undefined,
    }),
  },
});

export const {
  setRevealPII,
  setRequestId,
  setRequestStatus,
  setRequestFrom,
  setRequestTo,
  setPage,
  setVerbose,
  setSortField,
  setSortDirection,
  clearAllFilters,
  clearSortFields,
} = subjectRequestsSlice.actions;

export const selectRevealPII = (state: RootState) =>
  state.subjectRequests.revealPII;
export const selectRequestStatus = (state: RootState) =>
  state.subjectRequests.status;

export const selectPrivacyRequestFilters = (
  state: RootState
): PrivacyRequestParams => ({
  status: state.subjectRequests.status,
  id: state.subjectRequests.id,
  from: state.subjectRequests.from,
  to: state.subjectRequests.to,
  page: state.subjectRequests.page,
  size: state.subjectRequests.size,
  verbose: state.subjectRequests.verbose,
  sort_direction: state.subjectRequests.sort_direction,
  sort_field: state.subjectRequests.sort_field,
});

export const { reducer } = subjectRequestsSlice;
