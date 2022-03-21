import { configureStore } from '@reduxjs/toolkit';

import { setupListeners } from '@reduxjs/toolkit/query/react';
import { subjectRequestApi } from '../features/subject-requests/subject-requests.slice';

export const store = configureStore({
  reducer: {
    [subjectRequestApi.reducerPath]: subjectRequestApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(subjectRequestApi.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

setupListeners(store.dispatch);
