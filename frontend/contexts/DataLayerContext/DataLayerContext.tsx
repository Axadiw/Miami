import { createContext, ReactNode, useContext, useMemo } from 'react';
import { UseQueryResult } from '@tanstack/react-query/build/modern/index';
import { useAppGetVersion, UseGetAppVersionResult } from '@/api/useAppGetVersion';
import {
  useCheckIfLoginTokenIsValid,
  UseCheckIfLoginValidResult,
} from '@/api/useCheckIfLoginTokenIsValid';
import { useGetAccountInfo, UseGetAccountInfoResult } from '@/api/useGetAccountInfo';
import { useLoginUser, UseLoginUserResult } from '@/api/useLoginUser';
import { useRegisterUser, UseRegisterUserResult } from '@/api/useRegisterUser';
import { useSaveAccountInfo, UseSaveAccountInfoResult } from '@/api/useSaveAccountInfo';
import { useChangePassword, UseChangePasswordResult } from '@/api/useChangePassword';
import {
  GetTimeframesProps,
  GetTimeframesResponse,
  useGetTimeframes,
} from '@/api/useGetTimeframes';
import { GetSymbolsProps, GetSymbolsResponse, useGetSymbols } from '@/api/useGetSymbols';
import { GetOHLCVsProps, GetOHLCVsResponse, useGetOHLCVs } from '@/api/useGetOHLCVs';

export interface DataLayer {
  useAppGetVersion: () => UseGetAppVersionResult;
  useCheckIfLoginTokenIsValid: () => UseCheckIfLoginValidResult;
  useGetAccountInfo: () => UseGetAccountInfoResult;
  useLoginUser: () => UseLoginUserResult;
  useRegisterUser: () => UseRegisterUserResult;
  useSaveAccountInfo: () => UseSaveAccountInfoResult;
  useChangePassword: () => UseChangePasswordResult;
  useGetOHLCVs: (props: GetOHLCVsProps) => UseQueryResult<GetOHLCVsResponse, Error>;
  useGetSymbols: (props: GetSymbolsProps) => UseQueryResult<GetSymbolsResponse, Error>;
  useGetTimeframes: (props: GetTimeframesProps) => UseQueryResult<GetTimeframesResponse, Error>;
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
  const changePassword = useChangePassword();
  const getOHLCVs = useGetOHLCVs;
  const getSymbols = useGetSymbols;
  const getTimeframes = useGetTimeframes;
  const value = useMemo(
    () => ({
      useAppGetVersion: () => appGetVersion,
      useCheckIfLoginTokenIsValid: () => checkIfLoginTokenIsValid,
      useGetAccountInfo: () => getAccountInfo,
      useLoginUser: () => loginUser,
      useRegisterUser: () => registerUser,
      useSaveAccountInfo: () => saveAccountInfo,
      useChangePassword: () => changePassword,
      useGetOHLCVs: (props: GetOHLCVsProps) => getOHLCVs(props),
      useGetSymbols: (props: GetSymbolsProps) => getSymbols(props),
      useGetTimeframes: (props: GetTimeframesProps) => getTimeframes(props),
    }),
    [
      appGetVersion,
      changePassword,
      checkIfLoginTokenIsValid,
      getAccountInfo,
      getOHLCVs,
      getSymbols,
      getTimeframes,
      loginUser,
      registerUser,
      saveAccountInfo,
    ]
  );

  return <DataLayerContext.Provider value={value}>{children}</DataLayerContext.Provider>;
};
