import axios from 'axios';
import { useMutation, UseMutationResult, useQueryClient } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';
import { useLoginContext } from '@/contexts/LoginContext/LoginContext';
import { AccountInfoCacheKey } from '@/api/useGetAccountInfo';
import { UserConfig } from '@/app/account/components/userConfig/userConfigTab';

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
        twitter_id: info.twitterId,
        ui_timezone: info.uiTimezone,
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
