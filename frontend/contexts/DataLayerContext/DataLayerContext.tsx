import { createContext, ReactNode, useContext, useMemo } from 'react';
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

export interface DataLayer {
  useAppGetVersion: () => UseGetAppVersionResult;
  useCheckIfLoginTokenIsValid: () => UseCheckIfLoginValidResult;
  useGetAccountInfo: () => UseGetAccountInfoResult;
  useLoginUser: () => UseLoginUserResult;
  useRegisterUser: () => UseRegisterUserResult;
  useSaveAccountInfo: () => UseSaveAccountInfoResult;
  useChangePassword: () => UseChangePasswordResult;
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
  const value = useMemo(
    () => ({
      useAppGetVersion: () => appGetVersion,
      useCheckIfLoginTokenIsValid: () => checkIfLoginTokenIsValid,
      useGetAccountInfo: () => getAccountInfo,
      useLoginUser: () => loginUser,
      useRegisterUser: () => registerUser,
      useSaveAccountInfo: () => saveAccountInfo,
      useChangePassword: () => changePassword,
    }),
    [
      appGetVersion,
      changePassword,
      checkIfLoginTokenIsValid,
      getAccountInfo,
      loginUser,
      registerUser,
      saveAccountInfo,
    ]
  );

  return <DataLayerContext.Provider value={value}>{children}</DataLayerContext.Provider>;
};
