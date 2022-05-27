import { configureStore } from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query/react';

import { STORED_CREDENTIALS_KEY } from '../constants';
import {
  authApi,
  AuthState,
  credentialStorage,
  reducer as authReducer,
} from '../features/auth';
import {
  privacyRequestApi,
  reducer as privacyRequestsReducer,
} from '../features/privacy-requests';
import {
  reducer as userManagementReducer,
  userApi,
} from '../features/user-management';

let storedAuthState: AuthState | undefined;
if (typeof window !== 'undefined' && 'localStorage' in window) {
  const storedAuthStateString = localStorage.getItem(STORED_CREDENTIALS_KEY);
  if (storedAuthStateString) {
    try {
      storedAuthState = JSON.parse(storedAuthStateString);
    } catch (error) {
      // eslint-disable-next-line no-console
      console.log(error);
    }
  }
}

const store = configureStore({
  reducer: {
    [privacyRequestApi.reducerPath]: privacyRequestApi.reducer,
    subjectRequests: privacyRequestsReducer,
    [userApi.reducerPath]: userApi.reducer,
    [authApi.reducerPath]: authApi.reducer,
    userManagement: userManagementReducer,
    auth: authReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(
      credentialStorage.middleware,
      privacyRequestApi.middleware,
      userApi.middleware,
      authApi.middleware
    ),
  devTools: true,
  preloadedState: {
    auth: storedAuthState,
  },
});

setupListeners(store.dispatch);

export type RootState = ReturnType<typeof store.getState>;

export default store;
