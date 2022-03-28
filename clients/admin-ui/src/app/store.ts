import { configureStore } from '@reduxjs/toolkit';
import { createWrapper } from 'next-redux-wrapper';

import { setupListeners } from '@reduxjs/toolkit/query/react';
import subjectRequestsReducer, {
  subjectRequestApi,
} from '../features/subject-requests/subject-requests.slice';
import userReducer from '../features/user/user.slice';

const makeStore = () => {
  const store = configureStore({
    reducer: {
      [subjectRequestApi.reducerPath]: subjectRequestApi.reducer,
      subjectRequests: subjectRequestsReducer,
      user: userReducer,
    },
    middleware: (getDefaultMiddleware) =>
      getDefaultMiddleware().concat(subjectRequestApi.middleware),
    devTools: true,
  });
  console.log(store);
  setupListeners(store.dispatch);
  return store;
};

export type AppStore = ReturnType<typeof makeStore>;
export type AppState = ReturnType<AppStore['getState']>;

export const wrapper = createWrapper<AppStore>(makeStore);
