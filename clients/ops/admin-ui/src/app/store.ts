/* eslint-disable @typescript-eslint/no-unused-vars */
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

import { authApi, reducer as authReducer } from "../features/auth";
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

const createNoopStorage = () => ({
  getItem(_key: any) {
    return Promise.resolve(null);
  },
  setItem(_key: any, value: any) {
    return Promise.resolve(value);
  },
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

const rootReducer = (state: any, action: AnyAction) =>
  combineReducers(reducer)(
    action.type === "auth/logout" ? undefined : state,
    action
  );

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

export const makeStore = () =>
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
    devTools: process.env.NODE_ENV !== "production",
  });

const store = makeStore();

export const persistor = persistStore(store);

setupListeners(store.dispatch);

export default store;
