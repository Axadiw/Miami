import { createContext, ReactNode, useContext, useMemo } from 'react';
import { UseMutationResult, UseQueryResult } from '@tanstack/react-query';
import { AxiosResponse } from 'axios';
import { useAppGetVersion } from '@/api/useAppGetVersion';
import { useCheckIfLoginTokenIsValid } from '@/api/useCheckIfLoginTokenIsValid';
import { useGetAccountInfo } from '@/api/useGetAccountInfo';
import { LoginProps, LoginResponse, useLoginUser } from '@/api/useLoginUser';
import { RegisterProps, RegisterResponse, useRegisterUser } from '@/api/useRegisterUser';
import { useSaveAccountInfo } from '@/api/useSaveAccountInfo';
import { UserConfig } from '@/app/account/accountPage';

export interface DataLayer {
  useAppGetVersion: () => UseQueryResult<string, Error>;
  useCheckIfLoginTokenIsValid: () => UseQueryResult<boolean, Error>;
  useGetAccountInfo: () => UseQueryResult<UserConfig, Error>;
  useLoginUser: () => UseMutationResult<LoginResponse, Error, LoginProps, unknown>;
  useRegisterUser: () => UseMutationResult<RegisterResponse, Error, RegisterProps, unknown>;
  useSaveAccountInfo: () => UseMutationResult<AxiosResponse<any, any>, Error, UserConfig, unknown>;
}

export const DataLayerContext = createContext<DataLayer>({} as DataLayer);

export const useDataLayerContext = () => useContext(DataLayerContext);

export const DataLayerContextProvider = ({ children }: { children: ReactNode }) => {
  const appGetVersion = useAppGetVersion();
  const checkIfLoginTokenIsValid = useCheckIfLoginTokenIsValid();
  const getAccountInfo = useGetAccountInfo();
  const loginUser = useLoginUser();
  const registerUser = useRegisterUser();
  const saveAccountInfo = useSaveAccountInfo();
  const value = useMemo(
    () => ({
      useAppGetVersion: () => appGetVersion,
      useCheckIfLoginTokenIsValid: () => checkIfLoginTokenIsValid,
      useGetAccountInfo: () => getAccountInfo,
      useLoginUser: () => loginUser,
      useRegisterUser: () => registerUser,
      useSaveAccountInfo: () => saveAccountInfo,
    }),
    [
      appGetVersion,
      checkIfLoginTokenIsValid,
      getAccountInfo,
      loginUser,
      registerUser,
      saveAccountInfo,
    ]
  );

  return <DataLayerContext.Provider value={value}>{children}</DataLayerContext.Provider>;
};
