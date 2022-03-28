import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { HYDRATE } from 'next-redux-wrapper';
import { AppState } from '../../app/store';

import {
  PrivacyRequest,
  PrivacyRequestResponse,
  PrivacyRequestStatus,
} from './types';

interface PrivacyRequestParams {
  status?: PrivacyRequestStatus;
}

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
      query: ({ status }) => ({
        url: `privacy-request`,
        params: {
          include_identities: true,
          status,
        },
      }),
      transformResponse: (response: PrivacyRequestResponse) => response.items,
    }),
  }),
});

export const { useGetAllPrivacyRequestsQuery } = privacyRequestApi;

// Subject requests state (filters, etc.)
interface SubjectRequestsState {
  revealPII: boolean;
  status?: PrivacyRequestStatus;
  id?: string;
}

const initialState: SubjectRequestsState = {
  revealPII: false,
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

export const { setRevealPII, setRequestId, setRequestStatus, clearAllFilters } =
  subjectRequestsSlice.actions;

export const selectRevealPII = (state: AppState) =>
  state.subjectRequests.revealPII;
export const selectRequestStatus = (state: AppState) =>
  state.subjectRequests.status;

export const selectPrivacyRequestFilters = (
  state: AppState
): PrivacyRequestParams => ({
  status: state.subjectRequests.status,
});

export default subjectRequestsSlice.reducer;
