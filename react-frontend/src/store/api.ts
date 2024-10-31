import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { GenerateContentResponse, PreviewImageResponse } from './types';

export const api = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: 'http://127.0.0.1:5000/' }),
  endpoints: (builder) => ({
    generateContent: builder.mutation<GenerateContentResponse, string>({
      query: (url) => ({
        url: `generate-content/?url=${encodeURIComponent(url)}`,
        headers: {"Access-Control-Allow-Origin": "*"}
      }),
    }),
    getPreviewImage: builder.query<PreviewImageResponse, string>({
      query: (url) => `preview-img/?url=${encodeURIComponent(url)}`,
    }),
  }),
});

export const { useGenerateContentMutation, useGetPreviewImageQuery } = api;