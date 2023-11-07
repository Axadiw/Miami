import { UseLoginUserResult } from '@/api/useLoginUser';
import { UseRegisterUserResult } from '@/api/useRegisterUser';
import { UseGetAppVersionResult } from '@/api/useAppGetVersion';
import { UseCheckIfLoginValidResult } from '@/api/useCheckIfLoginTokenIsValid';
import { UseGetAccountInfoResult } from '@/api/useGetAccountInfo';
import { UseSaveAccountInfoResult } from '@/api/useSaveAccountInfo';
import { MockedMutationResult } from '@/contexts/DataLayerContext/__testing__/MockedMutationResult';
import { MockedQueryResult } from '@/contexts/DataLayerContext/__testing__/MockedQueryResult';
import { DataLayer } from '@/contexts/DataLayerContext/DataLayerContext';
import { UseChangePasswordResult } from '@/api/useChangePassword';

export class MockedDataLayerBuilder {
  private useAppGetVersion = jest.fn<UseGetAppVersionResult, []>();
  private useCheckIfLoginTokenIsValid = jest.fn<UseCheckIfLoginValidResult, []>();
  private useGetAccountInfo = jest.fn<UseGetAccountInfoResult, []>();
  private useLoginUser = jest.fn<UseLoginUserResult, []>();
  private useRegisterUser = jest.fn<UseRegisterUserResult, []>();
  private useSaveAccountInfo = jest.fn<UseSaveAccountInfoResult, []>();
  private useChangePassword = jest.fn<UseChangePasswordResult, []>();

  loginUserReturn(
    result: UseLoginUserResult = MockedMutationResult(
      { login: '', password: '' },
      { token: 'newToken' }
    )
  ) {
    this.useLoginUser.mockReturnValue(result);
    return this;
  }

  appGetVersionReturns(result: UseGetAppVersionResult = MockedQueryResult('TestVersion')) {
    this.useAppGetVersion.mockReturnValue(result);
    return this;
  }

  checkIfLoginTokenIsValidReturns(result: UseCheckIfLoginValidResult = MockedQueryResult(true)) {
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
      useChangePassword: this.useChangePassword,
    };
  }
}
