import { configureStore } from '@reduxjs/toolkit';

import subjectRequestsReducer from '../features/subject-requests/subject-requests.slice';

export const store = configureStore({
  reducer: {
    subjectRequests: subjectRequestsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
