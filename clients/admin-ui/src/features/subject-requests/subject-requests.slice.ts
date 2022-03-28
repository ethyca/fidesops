import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { HYDRATE } from 'next-redux-wrapper';
import { AppState } from '../../app/store';

import { SubjectRequestResponse } from './types';

// Subject requests API
export const subjectRequestApi = createApi({
  reducerPath: 'subjectRequestApi',
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
    getAllSubjectRequests: build.query<SubjectRequestResponse, null>({
      query: () => ({
        url: `privacy-request`,
        params: {
          include_identities: true,
        },
      }),
    }),
  }),
});

export const { useGetAllSubjectRequestsQuery } = subjectRequestApi;

// Subject requests state (filters, etc.)
interface SubjectRequestsState {
  revealPII: boolean;
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
  },
  extraReducers: {
    [HYDRATE]: (state, action) => ({
      ...state,
      ...action.payload.subjectRequests,
    }),
  },
});

export const { setRevealPII } = subjectRequestsSlice.actions;

export const selectRevealPII = (state: AppState) =>
  state.subjectRequests.revealPII;

export default subjectRequestsSlice.reducer;
