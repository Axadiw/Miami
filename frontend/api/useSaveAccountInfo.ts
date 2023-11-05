import axios from 'axios';
import { useMutation, UseMutationResult, useQueryClient } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';
import { UserConfig } from '@/app/account/accountPage';
import { useLoginContext } from '@/contexts/LoginContext/LoginContext';
import { AccountInfoCacheKey } from '@/api/useGetAccountInfo';

export type UseSaveAccountInfoResult = UseMutationResult<
  SaveAccountInfoResponse,
  Error,
  UserConfig,
  unknown
>;

export interface SaveAccountInfoResponse {
  message: string;
}

export const saveAccountInfo = async (token: string | null | undefined, info: UserConfig) => {
  if (!token) {
    return Promise.reject(NotLoggedInError);
  }

  try {
    return (await axios.request({
      method: 'post',
      url: `${BASE_URL}/save_config`,
      headers: {
        'Content-Type': 'application/json',
        'x-access-tokens': token,
      },
      data: JSON.stringify({
        '3commas_account': info.threeCommasAccountId,
        '3commas_api_key': info.threeCommasApiKey,
        '3commas_secret': info.threeCommasSecret,
        bybit_api_key: info.byBitApiKey,
        bybit_api_secret: info.byBitApiSecret,
      }),
    })) as SaveAccountInfoResponse;
  } catch (error: any) {
    throw new Error(error.response.data.error);
  }
};

export const useSaveAccountInfo = (): UseSaveAccountInfoResult => {
  const { loginToken } = useLoginContext();
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (info: UserConfig) => saveAccountInfo(loginToken, info),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [AccountInfoCacheKey] });
    },
  });
};
