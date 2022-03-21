import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from '../../app/store';

export type SubjectRequestStatus =
  | 'error'
  | 'denied'
  | 'in-progress'
  | 'new'
  | 'completed';

interface SubjectRequest {
  status: SubjectRequestStatus;
  identity: {
    email?: string;
    phone?: string;
  };
  created_at: string;
  reviewed_by: string;
  id: string;
}

interface SubjectRequestsState {
  requests: SubjectRequest[];
}

const initialState: SubjectRequestsState = {
  requests: [],
};

export const subjectRequestsSlice = createSlice({
  name: 'subjectRequests',
  initialState,
  reducers: {
    loadRequests: (state, action: PayloadAction<SubjectRequest[]>) => {
      Object.assign(state, { requests: action.payload });
    },
  },
});

export const { loadRequests } = subjectRequestsSlice.actions;

export const subjectRequests = (state: RootState) =>
  state.subjectRequests.requests;

export default subjectRequestsSlice.reducer;
