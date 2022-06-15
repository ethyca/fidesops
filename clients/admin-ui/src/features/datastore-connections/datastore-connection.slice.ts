import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

import type { RootState } from "../../app/store";
import { BASE_URL, CONNECTION_ROUTE } from "../../constants";
import { selectToken } from "../auth";
import { PrivacyRequestParams } from "../privacy-requests/types";
import {
  DatastoreConnection,
  DatastoreConnectionParams,
  DatastoreConnectionResponse,
  DatastoreConnectionStatus,
} from "./types";

function mapFiltersToSearchParams({
  status,
  id,
  from,
  to,
  page,
  size,
  verbose,
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
    ...(status ? { status } : {}),
    ...(id ? { request_id: id } : {}),
    ...(fromISO ? { created_gt: fromISO.toISOString() } : {}),
    ...(toISO ? { created_lt: toISO.toISOString() } : {}),
    ...(page ? { page: `${page}` } : {}),
    ...(typeof size !== "undefined" ? { size: `${size}` } : {}),
    ...(verbose ? { verbose } : {}),
  };
}

export const datastoreConnectionApi = createApi({
  reducerPath: "datastoreConnectionApi",
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_URL,
    prepareHeaders: (headers, { getState }) => {
      const token = selectToken(getState() as RootState);
      headers.set("Access-Control-Allow-Origin", "*");
      if (token) {
        headers.set("authorization", `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ["DatastoreConnection"],
  endpoints: (build) => ({
    getAllDatastoreConnections: build.query<
      DatastoreConnectionResponse,
      Partial<DatastoreConnectionParams>
    >({
      query: (filters) => ({
        url: CONNECTION_ROUTE,
        params: mapFiltersToSearchParams(filters),
      }),
      providesTags: () => ["DatastoreConnection"],
    }),
    getDatastoreConnectionById: build.query<DatastoreConnection, string>({
      query: (id) => ({
        url: `${CONNECTION_ROUTE}/${id}`,
      }),
      providesTags: () => ["DatastoreConnection"],
    }),
    getDatastoreConnectionStatus: build.query<
      DatastoreConnectionStatus,
      string
    >({
      query: (id) => ({
        url: `${CONNECTION_ROUTE}/${id}/test`,
      }),
      providesTags: () => ["DatastoreConnection"],
    }),
    patchDatastoreConnections: build.mutation({
      query: () => ({
        url: CONNECTION_ROUTE,
        method: "PATCH",
        body: {},
      }),
      invalidatesTags: () => ["DatastoreConnection"],
    }),
    deleteDatastoreConnection: build.mutation({
      query: (id) => ({
        url: `${CONNECTION_ROUTE}/${id}`,
        method: "DELETE",
      }),
      invalidatesTags: () => ["DatastoreConnection"],
    }),
    updateDatastoreConnectionSecrets: build.mutation({
      query: (id) => ({
        url: `${CONNECTION_ROUTE}/${id}/secret`,
        method: "PUT",
        body: {},
      }),
      invalidatesTags: () => ["DatastoreConnection"],
    }),
  }),
});

export const {
  useGetAllDatastoreConnectionsQuery,
  // useGetDatastoreConnectionByIdQuery,
  // usePatchDatastoreConnectionsMutation,
  // useDeleteDatastoreConnectionMutation,
} = datastoreConnectionApi;
