import {
  AnyAction,
  combineReducers,
  configureStore,
  StateFromReducersMapObject,
} from "@reduxjs/toolkit";
import { setupListeners } from "@reduxjs/toolkit/query/react";
import {
  FLUSH,
  PAUSE,
  PERSIST,
  persistReducer,
  persistStore,
  PURGE,
  REGISTER,
  REHYDRATE,
} from "redux-persist";
import createWebStorage from "redux-persist/lib/storage/createWebStorage";

import { STORAGE_ROOT_KEY } from "../constants";
import { authApi, AuthState, reducer as authReducer } from "../features/auth";
import {
  connectionTypeApi,
  reducer as connectionTypeReducer,
} from "../features/connection-type";
import {
  datastoreConnectionApi,
  reducer as datastoreConnectionReducer,
} from "../features/datastore-connections";
import {
  privacyRequestApi,
  reducer as privacyRequestsReducer,
} from "../features/privacy-requests";
import {
  reducer as userManagementReducer,
  userApi,
} from "../features/user-management";

/**
 * To prevent the "redux-perist failed to create sync storage. falling back to noop storage"
 * console message within Next.js, the following snippet is required.
 * {@https://mightycoders.xyz/redux-persist-failed-to-create-sync-storage-falling-back-to-noop-storage}
 */
const createNoopStorage = () => ({
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  getItem(_key: any) {
    return Promise.resolve(null);
  },
  setItem(_key: any, value: any) {
    return Promise.resolve(value);
  },
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  removeItem(_key: any) {
    return Promise.resolve();
  },
});

const storage =
  typeof window !== "undefined"
    ? createWebStorage("local")
    : createNoopStorage();

const reducer = {
  [privacyRequestApi.reducerPath]: privacyRequestApi.reducer,
  subjectRequests: privacyRequestsReducer,
  [userApi.reducerPath]: userApi.reducer,
  [authApi.reducerPath]: authApi.reducer,
  userManagement: userManagementReducer,
  [datastoreConnectionApi.reducerPath]: datastoreConnectionApi.reducer,
  datastoreConnections: datastoreConnectionReducer,
  auth: authReducer,
  [connectionTypeApi.reducerPath]: connectionTypeApi.reducer,
  connectionType: connectionTypeReducer,
};

const rootReducer = (state: any, action: AnyAction) => {
  if (action.type === "auth/logout") {
    storage.removeItem(STORAGE_ROOT_KEY);
    // eslint-disable-next-line no-param-reassign
    state = {};
  }
  return combineReducers(reducer)(state, action);
};

const persistConfig = {
  key: "root",
  storage,
  blacklist: [
    privacyRequestApi.reducerPath,
    userApi.reducerPath,
    authApi.reducerPath,
    datastoreConnectionApi.reducerPath,
    connectionTypeApi.reducerPath,
  ],
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

export type RootState = StateFromReducersMapObject<typeof reducer>;

export const makeStore = (preloadedState?: Partial<RootState>) =>
  configureStore({
    reducer: persistedReducer,
    middleware: (getDefaultMiddleware) =>
      getDefaultMiddleware({
        serializableCheck: {
          ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
        },
      }).concat(
        privacyRequestApi.middleware,
        userApi.middleware,
        authApi.middleware,
        datastoreConnectionApi.middleware,
        connectionTypeApi.middleware
      ),
    devTools: true,
    preloadedState,
  });

let storedAuthState: AuthState | undefined;
if (typeof window !== "undefined" && "localStorage" in window) {
  const storedAuthStateString = localStorage.getItem(STORAGE_ROOT_KEY);
  if (storedAuthStateString) {
    try {
      storedAuthState = JSON.parse(storedAuthStateString);
    } catch (error) {
      // TODO: build in formal error logging system
      // eslint-disable-next-line no-console
      console.error(error);
    }
  }
}

const store = makeStore({
  auth: storedAuthState,
});

export const persistor = persistStore(store);

setupListeners(store.dispatch);

export default store;
