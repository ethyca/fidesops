import { configureStore } from '@reduxjs/toolkit';
import { createWrapper } from 'next-redux-wrapper';

import { setupListeners } from '@reduxjs/toolkit/query/react';
import privacyRequestsReducer, {
  privacyRequestApi,
} from '../features/privacy-requests/privacy-requests.slice';
import userReducer from '../features/user/user.slice';

const makeStore = () => {
  const store = configureStore({
    reducer: {
      [privacyRequestApi.reducerPath]: privacyRequestApi.reducer,
      subjectRequests: privacyRequestsReducer,
      user: userReducer,
    },
    middleware: (getDefaultMiddleware) =>
      getDefaultMiddleware().concat(privacyRequestApi.middleware),
    devTools: true,
  });
  setupListeners(store.dispatch);
  return store;
};

export type AppStore = ReturnType<typeof makeStore>;
export type AppState = ReturnType<AppStore['getState']>;

export const wrapper = createWrapper<AppStore>(makeStore);
