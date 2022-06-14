/**
 * Taken from https://redux-toolkit.js.org/rtk-query/usage-with-typescript#inline-error-handling-example
 */

import { FetchBaseQueryError } from '@reduxjs/toolkit/query';
import { fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import {RootState} from "../../app/store";
import {selectToken} from "../auth";

/**
 * Type predicate to narrow an unknown error to `FetchBaseQueryError`
 */
export function isFetchBaseQueryError(
  error: unknown
): error is FetchBaseQueryError {
  return typeof error === 'object' && error != null && 'status' in error;
}

/**
 * Type predicate to narrow an unknown error to an object with a string 'message' property
 */
export function isErrorWithMessage(
  error: unknown
): error is { message: string } {
  return (
    typeof error === 'object' &&
    error != null &&
    'message' in error &&
    typeof (error as any).message === 'string'
  );
}


export function buildBaseQuery() {
  return fetchBaseQuery({
    baseUrl: process.env.NEXT_PUBLIC_FIDESOPS_API!,
    prepareHeaders: (headers, {getState}) => {
      const token = selectToken(getState() as RootState);
      headers.set('Access-Control-Allow-Origin', '*');
      headers.set('X-Fides-Source', 'fidesops-admin-ui');
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
  })
}

// generic error of the structure we expect from the Fidesops backend
interface ResponseError {
  data: {
    detail: string;
  };
}

interface ErrorDetail {
  loc: string[];
  msg: string;
  type: string;
}

interface ValidationError {
  data: {
    detail: ErrorDetail[];
  };
}

/**
 * Custom type predicate to see if the error has details as returned by the Fidesops API
 * @param error
 * @returns
 */
export function isErrorWithDetail(error: unknown): error is ResponseError {
  return (
    typeof error === 'object' &&
    error != null &&
    'data' in error &&
    typeof (error as any).data.detail === 'string'
  );
}

export function isErrorWithDetailArray(
  error: unknown
): error is ValidationError {
  return (
    typeof error === 'object' &&
    error != null &&
    'data' in error &&
    Array.isArray((error as any).data.detail)
  );
}
