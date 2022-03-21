import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

import { SubjectRequest } from './types';

// Define a service using a base URL and expected endpoints
export const subjectRequestApi = createApi({
  reducerPath: 'subjectRequestApi',
  baseQuery: fetchBaseQuery({ baseUrl: 'http://localhost/api/v1' }),
  endpoints: (build) => ({
    getAllSubjectRequests: build.query<SubjectRequest, null>({
      query: () => `subject-requests/preview`,
    }),
  }),
});

// Export hooks for usage in functional components, which are
// auto-generated based on the defined endpoints
export const { useGetAllSubjectRequestsQuery } = subjectRequestApi;
