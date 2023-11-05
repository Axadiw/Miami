import { UseMutationResult, UseQueryResult } from '@tanstack/react-query';
import { AxiosResponse } from 'axios';
import { UserConfig } from '@/app/account/accountPage';
import { LoginProps, LoginResponse } from '@/api/useLoginUser';
import { RegisterProps, RegisterResponse } from '@/api/useRegisterUser';
import { DataLayer } from '@/contexts/DataLayerContext';

export class MockedDataLayerBuilder {
  private useAppGetVersion = jest.fn<UseQueryResult<string, Error>, []>();
  private useCheckIfLoginTokenIsValid = jest.fn<UseQueryResult<boolean, Error>, []>();
  private useGetAccountInfo = jest.fn<UseQueryResult<UserConfig, Error>, []>();
  private useLoginUser = jest.fn<
    UseMutationResult<LoginResponse, Error, LoginProps, unknown>,
    []
  >();
  private useRegisterUser = jest.fn<
    UseMutationResult<RegisterResponse, Error, RegisterProps, unknown>,
    []
  >();
  private useSaveAccountInfo = jest.fn<
    UseMutationResult<AxiosResponse<any, any>, Error, UserConfig, unknown>,
    []
  >();

  loginUserReturn(
    result: UseMutationResult<LoginResponse, Error, LoginProps, unknown> = {
      data: { token: 'newToken' },
      isError: false,
      variables: { login: '', password: '' },
      error: null,
      isPending: false,
      isIdle: false,
      isPaused: false,
      isSuccess: true,
      status: 'success',
      failureCount: 0,
      failureReason: null,
      mutateAsync: jest.fn().mockReturnValue(Promise.resolve({ token: 'newToken' })),
      mutate: jest.fn(),
      reset: jest.fn(),
      context: null,
      submittedAt: 0,
    }
  ) {
    this.useLoginUser.mockReturnValue(result);
    return this;
  }

  appGetVersionReturns(
    result: UseQueryResult<string, Error> = {
      data: 'testVersion',
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
    }
  ) {
    this.useAppGetVersion.mockReturnValue(result);
    return this;
  }

  checkIfLoginTokenIsValidReturns(
    result: UseQueryResult<boolean, Error> = {
      data: true,
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
    }
  ) {
    this.useCheckIfLoginTokenIsValid.mockReturnValue(result);
    return this;
  }

  build(): DataLayer {
    return {
      useAppGetVersion: this.useAppGetVersion,
      useCheckIfLoginTokenIsValid: this.useCheckIfLoginTokenIsValid,
      useGetAccountInfo: this.useGetAccountInfo,
      useLoginUser: this.useLoginUser,
      useRegisterUser: this.useRegisterUser,
      useSaveAccountInfo: this.useSaveAccountInfo,
    };
  }
}
