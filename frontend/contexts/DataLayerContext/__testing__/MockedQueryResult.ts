import { UseQueryResult } from '@tanstack/react-query';

export function MockedQueryResult<ReturnType>(returnValue: ReturnType) {
  return {
    data: returnValue,
    isError: false,
    error: null,
    isPending: false,
    isPaused: false,
    isSuccess: true,
    status: 'success',
    failureCount: 0,
    failureReason: null,
    isLoadingError: false,
    isFetched: true,
    isStale: false,
    isLoading: false,
    isFetching: false,
    isPlaceholderData: false,
    isFetchedAfterMount: false,
    isRefetching: false,
    isRefetchError: false,
    dataUpdatedAt: 0,
    errorUpdatedAt: 0,
    errorUpdateCount: 0,
    fetchStatus: 'idle',
    refetch: jest.fn(),
    isInitialLoading: false,
    promise: Promise.resolve(returnValue),
  } as UseQueryResult<ReturnType, Error>;
}
