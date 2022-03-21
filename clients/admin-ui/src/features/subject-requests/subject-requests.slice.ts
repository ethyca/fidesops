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
  identity: string;
  timeReceived: string;
  reviewer: string;
  id: string;
}

interface SubjectRequestsState {
  requests: SubjectRequest[];
}

const initialState: SubjectRequestsState = {
  requests: [
    {
      status: 'error',
      identity: 'james.braithwaite@email.com',
      timeReceived: 'August 4, 2021, 09:35:46 PST',
      reviewer: 'Sammie_Shanahan@gmail.com',
      id: '123',
    },
    {
      status: 'denied',
      identity: '555-325-685-126',
      timeReceived: 'August 4, 2021, 09:35:46 PST',
      reviewer: 'Richmond33@yahoo.com',
      id: '456',
    },
    {
      status: 'in-progress',
      identity: 'mary.jane.@email.com',
      timeReceived: 'August 4, 2021, 09:35:46 PST',
      reviewer: 'Oceane.Volkman@gmail.com',
      id: '789',
    },
    {
      status: 'new',
      identity: 'jeremiah.stones@email.com',
      timeReceived: 'August 4, 2021, 09:35:46 PST',
      reviewer: 'Verdie64@yahoo.com',
      id: '012',
    },
    {
      status: 'completed',
      identity: '283-774-5003',
      timeReceived: 'August 4, 2021, 09:35:46 PST',
      reviewer: 'Maximo_Willms0@gmail.com',
      id: '345',
    },
  ],
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
