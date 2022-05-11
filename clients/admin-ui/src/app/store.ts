import { configureStore } from '@reduxjs/toolkit';
import { createWrapper } from 'next-redux-wrapper';

import { setupListeners } from '@reduxjs/toolkit/query/react';
import {
  reducer as privacyRequestsReducer,
  privacyRequestApi,
} from '../features/privacy-requests';
import { reducer as userReducer, userApi } from '../features/user';

const makeStore = () => {
  const store = configureStore({
    reducer: {
      [privacyRequestApi.reducerPath]: privacyRequestApi.reducer,
      subjectRequests: privacyRequestsReducer,
      [userApi.reducerPath]: userApi.reducer,
      user: userReducer,
    },
    middleware: (getDefaultMiddleware) =>
      getDefaultMiddleware().concat(
        privacyRequestApi.middleware,
        userApi.middleware
      ),
    devTools: true,
  });
  setupListeners(store.dispatch);
  return store;
};

export type AppStore = ReturnType<typeof makeStore>;
export type AppState = ReturnType<AppStore['getState']>;

export const wrapper = createWrapper<AppStore>(makeStore);
