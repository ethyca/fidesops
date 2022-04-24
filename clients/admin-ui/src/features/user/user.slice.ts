import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { HYDRATE } from 'next-redux-wrapper';
import type { AppState } from '../../app/store';

import {
  UserParams,
  UserResponse,
  UsersParams,
  UsersResponse,
  User,
} from './types';

export interface State {
  id: string;
  page: number;
  size: number;
  token: string | null;
}

const initialState: State = {
  id: '',
  page: 1,
  size: 25,
  token: null,
};

// User API
export const userApi = createApi({
  reducerPath: 'userApi',
  baseQuery: fetchBaseQuery({
    baseUrl: process.env.NEXT_PUBLIC_FIDESOPS_API!,
    prepareHeaders: (headers, { getState }) => {
      const { token } = (getState() as AppState).user;
      headers.set('Access-Control-Allow-Origin', '*');
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ['User'],
  endpoints: (build) => ({
    getAllUsers: build.query<
      UsersResponse,
      UsersParams
    >({
      query: () => ({ url: `users` }),
      providesTags: () => ['User'],
    }),
    getUserById: build.query<
      UserResponse,
      UserParams
    >({
      query: (id) => ({ url: `user/${id}` }),
      providesTags: () => ['User'],
    }),
    editUser: build.mutation<
      User,
      Partial<User> & Pick<User, 'id'>
    >({
      query: ({ id, ...patch }) => ({
        url: `user/${id}`,
        method: 'PATCH',
        body: patch,
      }),
      invalidatesTags: ['User'],
      // For optimistic update
      async onQueryStarted({ id, ...patch }, { dispatch, queryFulfilled }) {
        const patchResult = dispatch(
          userApi.util.updateQueryData('getUserById', { id }, (draft) => {
            Object.assign(draft, patch)
          })
        )
        try {
          await queryFulfilled
        } catch {
          patchResult.undo()
          /**
           * Alternatively, on failure you can invalidate the corresponding cache tags
           * to trigger a re-fetch:
           * dispatch(api.util.invalidateTags(['User']))
           */
        }
      },
    }),
    deleteUser: build.mutation<{ success: boolean; id: number }, number>({
      query: (id) => ({
        url: `user/${id}`,
        method: 'DELETE',
      }),
      // Invalidates all queries that subscribe to this User `id` only
      invalidatesTags: (result, error, id) => [{ type: 'User', id }],
    }),
  }),
});

export const {
  useGetAllUsersQuery,
  useGetUserByIdQuery,
  useEditUserMutation,
  useDeleteUserMutation,
} = userApi;

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    assignToken: (state, action: PayloadAction<string>) => ({
      ...state,
      token: action.payload,
    }),
    setUserId: (state, action: PayloadAction<string>) => ({
      ...state,
      page: initialState.page,
      id: action.payload,
    }),
  },
  extraReducers: {
    [HYDRATE]: (state, action) => ({
      ...state,
      ...action.payload.user,
    }),
  },
});

export const { assignToken, setUserId } = userSlice.actions;

export const selectUserToken = (state: AppState) => state.user.token;

export const { reducer } = userSlice;
