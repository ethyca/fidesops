import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { HYDRATE } from 'next-redux-wrapper';
import { AppState } from '../../app/store';

import {
  PrivacyRequest,
  PrivacyRequestParams,
  PrivacyRequestResponse,
  PrivacyRequestStatus,
} from './types';

// Helpers
export const mapFiltersToSearchParams = ({
  status,
  id,
  from,
  to,
}: PrivacyRequestParams) => ({
  include_identities: 'true',
  ...(status ? { status } : {}),
  ...(id ? { id } : {}),
  ...(from ? { created_gt: from } : {}),
  ...(to ? { created_lt: to } : {}),
});

// Subject requests API
export const privacyRequestApi = createApi({
  reducerPath: 'privacyRequestApi',
  baseQuery: fetchBaseQuery({
    baseUrl: 'http://0.0.0.0:8080/api/v1',
    prepareHeaders: (headers, { getState }) => {
      const { token } = (getState() as AppState).user;
      headers.set('Access-Control-Allow-Origin', '*');
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  endpoints: (build) => ({
    getAllPrivacyRequests: build.query<PrivacyRequest[], PrivacyRequestParams>({
      query: (filters) => ({
        url: `privacy-request`,
        params: mapFiltersToSearchParams(filters),
      }),
      transformResponse: (response: PrivacyRequestResponse) => response.items,
    }),
  }),
});

export const { useGetAllPrivacyRequestsQuery } = privacyRequestApi;

export const requestCSVDownload = ({
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
    `http://0.0.0.0:8080/api/v1/privacy-request?${new URLSearchParams({
      ...mapFiltersToSearchParams({
        id,
        from,
        to,
        status,
      }),
      download_csv: 'true',
    })}`,
    {
      headers: {
        'Access-Control-Allow-Origin': '*',
        Authorization: `Bearer ${token}`,
      },
    }
  )
    .then((res) => res.blob())
    .then((data) => {
      const a = document.createElement('a');
      a.href = window.URL.createObjectURL(data);
      a.download = 'privacy-requests.csv';
      a.click();
    });
};

// Subject requests state (filters, etc.)
interface SubjectRequestsState {
  revealPII: boolean;
  status?: PrivacyRequestStatus;
  id: string;
  from: string;
  to: string;
}

const initialState: SubjectRequestsState = {
  revealPII: false,
  id: '',
  from: '',
  to: '',
};

export const subjectRequestsSlice = createSlice({
  name: 'subjectRequests',
  initialState,
  reducers: {
    setRevealPII: (state, action: PayloadAction<boolean>) => ({
      ...state,
      revealPII: action.payload,
    }),
    setRequestStatus: (state, action: PayloadAction<PrivacyRequestStatus>) => ({
      ...state,
      status: action.payload,
    }),
    setRequestId: (state, action: PayloadAction<string>) => ({
      ...state,
      id: action.payload,
    }),
    setRequestFrom: (state, action: PayloadAction<string>) => ({
      ...state,
      from: action.payload,
    }),
    setRequestTo: (state, action: PayloadAction<string>) => ({
      ...state,
      to: action.payload,
    }),
    clearAllFilters: ({ revealPII }) => ({
      ...initialState,
      revealPII,
    }),
  },
  extraReducers: {
    [HYDRATE]: (state, action) => ({
      ...state,
      ...action.payload.subjectRequests,
    }),
  },
});

export const {
  setRevealPII,
  setRequestId,
  setRequestStatus,
  setRequestFrom,
  setRequestTo,
  clearAllFilters,
} = subjectRequestsSlice.actions;

export const selectRevealPII = (state: AppState) =>
  state.subjectRequests.revealPII;
export const selectRequestStatus = (state: AppState) =>
  state.subjectRequests.status;

export const selectPrivacyRequestFilters = (
  state: AppState
): PrivacyRequestParams => ({
  status: state.subjectRequests.status,
  id: state.subjectRequests.id,
  from: state.subjectRequests.from,
  to: state.subjectRequests.to,
});

export default subjectRequestsSlice.reducer;
