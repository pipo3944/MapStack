/**
 * Generated by orval v7.8.0 🍺
 * Do not edit manually.
 * MapStack API
 * AI学習プラットフォーム MapStack のバックエンドAPI
 * OpenAPI spec version: 0.1.0
 */
import {
  useQuery
} from '@tanstack/react-query';
import type {
  DataTag,
  DefinedInitialDataOptions,
  DefinedUseQueryResult,
  QueryClient,
  QueryFunction,
  QueryKey,
  UndefinedInitialDataOptions,
  UseQueryOptions,
  UseQueryResult
} from '@tanstack/react-query';

import { customInstance } from '../../mutator/custom-instance';




/**
 * @summary Root
 */
export const rootGet = (
    
 signal?: AbortSignal
) => {
      
      
      return customInstance<unknown>(
      {url: `/`, method: 'GET', signal
    },
      );
    }
  

export const getRootGetQueryKey = () => {
    return [`/`] as const;
    }

    
export const getRootGetQueryOptions = <TData = Awaited<ReturnType<typeof rootGet>>, TError = unknown>( options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof rootGet>>, TError, TData>>, }
) => {

const {query: queryOptions} = options ?? {};

  const queryKey =  queryOptions?.queryKey ?? getRootGetQueryKey();

  

    const queryFn: QueryFunction<Awaited<ReturnType<typeof rootGet>>> = ({ signal }) => rootGet(signal);

      

      

   return  { queryKey, queryFn, ...queryOptions} as UseQueryOptions<Awaited<ReturnType<typeof rootGet>>, TError, TData> & { queryKey: DataTag<QueryKey, TData, TError> }
}

export type RootGetQueryResult = NonNullable<Awaited<ReturnType<typeof rootGet>>>
export type RootGetQueryError = unknown


export function useRootGet<TData = Awaited<ReturnType<typeof rootGet>>, TError = unknown>(
  options: { query:Partial<UseQueryOptions<Awaited<ReturnType<typeof rootGet>>, TError, TData>> & Pick<
        DefinedInitialDataOptions<
          Awaited<ReturnType<typeof rootGet>>,
          TError,
          Awaited<ReturnType<typeof rootGet>>
        > , 'initialData'
      >, }
 , queryClient?: QueryClient
  ):  DefinedUseQueryResult<TData, TError> & { queryKey: DataTag<QueryKey, TData, TError> }
export function useRootGet<TData = Awaited<ReturnType<typeof rootGet>>, TError = unknown>(
  options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof rootGet>>, TError, TData>> & Pick<
        UndefinedInitialDataOptions<
          Awaited<ReturnType<typeof rootGet>>,
          TError,
          Awaited<ReturnType<typeof rootGet>>
        > , 'initialData'
      >, }
 , queryClient?: QueryClient
  ):  UseQueryResult<TData, TError> & { queryKey: DataTag<QueryKey, TData, TError> }
export function useRootGet<TData = Awaited<ReturnType<typeof rootGet>>, TError = unknown>(
  options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof rootGet>>, TError, TData>>, }
 , queryClient?: QueryClient
  ):  UseQueryResult<TData, TError> & { queryKey: DataTag<QueryKey, TData, TError> }
/**
 * @summary Root
 */

export function useRootGet<TData = Awaited<ReturnType<typeof rootGet>>, TError = unknown>(
  options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof rootGet>>, TError, TData>>, }
 , queryClient?: QueryClient 
 ):  UseQueryResult<TData, TError> & { queryKey: DataTag<QueryKey, TData, TError> } {

  const queryOptions = getRootGetQueryOptions(options)

  const query = useQuery(queryOptions , queryClient) as  UseQueryResult<TData, TError> & { queryKey: DataTag<QueryKey, TData, TError> };

  query.queryKey = queryOptions.queryKey ;

  return query;
}



/**
 * @summary Health Check
 */
export const healthCheckHealthGet = (
    
 signal?: AbortSignal
) => {
      
      
      return customInstance<unknown>(
      {url: `/health`, method: 'GET', signal
    },
      );
    }
  

export const getHealthCheckHealthGetQueryKey = () => {
    return [`/health`] as const;
    }

    
export const getHealthCheckHealthGetQueryOptions = <TData = Awaited<ReturnType<typeof healthCheckHealthGet>>, TError = unknown>( options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof healthCheckHealthGet>>, TError, TData>>, }
) => {

const {query: queryOptions} = options ?? {};

  const queryKey =  queryOptions?.queryKey ?? getHealthCheckHealthGetQueryKey();

  

    const queryFn: QueryFunction<Awaited<ReturnType<typeof healthCheckHealthGet>>> = ({ signal }) => healthCheckHealthGet(signal);

      

      

   return  { queryKey, queryFn, ...queryOptions} as UseQueryOptions<Awaited<ReturnType<typeof healthCheckHealthGet>>, TError, TData> & { queryKey: DataTag<QueryKey, TData, TError> }
}

export type HealthCheckHealthGetQueryResult = NonNullable<Awaited<ReturnType<typeof healthCheckHealthGet>>>
export type HealthCheckHealthGetQueryError = unknown


export function useHealthCheckHealthGet<TData = Awaited<ReturnType<typeof healthCheckHealthGet>>, TError = unknown>(
  options: { query:Partial<UseQueryOptions<Awaited<ReturnType<typeof healthCheckHealthGet>>, TError, TData>> & Pick<
        DefinedInitialDataOptions<
          Awaited<ReturnType<typeof healthCheckHealthGet>>,
          TError,
          Awaited<ReturnType<typeof healthCheckHealthGet>>
        > , 'initialData'
      >, }
 , queryClient?: QueryClient
  ):  DefinedUseQueryResult<TData, TError> & { queryKey: DataTag<QueryKey, TData, TError> }
export function useHealthCheckHealthGet<TData = Awaited<ReturnType<typeof healthCheckHealthGet>>, TError = unknown>(
  options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof healthCheckHealthGet>>, TError, TData>> & Pick<
        UndefinedInitialDataOptions<
          Awaited<ReturnType<typeof healthCheckHealthGet>>,
          TError,
          Awaited<ReturnType<typeof healthCheckHealthGet>>
        > , 'initialData'
      >, }
 , queryClient?: QueryClient
  ):  UseQueryResult<TData, TError> & { queryKey: DataTag<QueryKey, TData, TError> }
export function useHealthCheckHealthGet<TData = Awaited<ReturnType<typeof healthCheckHealthGet>>, TError = unknown>(
  options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof healthCheckHealthGet>>, TError, TData>>, }
 , queryClient?: QueryClient
  ):  UseQueryResult<TData, TError> & { queryKey: DataTag<QueryKey, TData, TError> }
/**
 * @summary Health Check
 */

export function useHealthCheckHealthGet<TData = Awaited<ReturnType<typeof healthCheckHealthGet>>, TError = unknown>(
  options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof healthCheckHealthGet>>, TError, TData>>, }
 , queryClient?: QueryClient 
 ):  UseQueryResult<TData, TError> & { queryKey: DataTag<QueryKey, TData, TError> } {

  const queryOptions = getHealthCheckHealthGetQueryOptions(options)

  const query = useQuery(queryOptions , queryClient) as  UseQueryResult<TData, TError> & { queryKey: DataTag<QueryKey, TData, TError> };

  query.queryKey = queryOptions.queryKey ;

  return query;
}



