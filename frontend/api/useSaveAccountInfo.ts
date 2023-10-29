import axios from 'axios';
import { BASE_URL } from '@/app/consts';
import { UserConfig } from '@/app/account/accountPage';
import { useLoginContext } from '@/contexts/LoginContext';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { AccountInfoCacheKey } from '@/api/useGetAccountInfo';

export const saveAccountInfo = async (token: string | null, info: UserConfig) => {
  if (token === null) {
    return Promise.reject(NotLoggedInError);
  }

  try {
    return await axios.request({
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
    });
  } catch (error: any) {
    throw new Error(error.response.data.error);
  }
};

export const useSaveAccountInfo = () => {
  const { loginToken } = useLoginContext();
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (info: UserConfig) => {
      return saveAccountInfo(loginToken, info);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [AccountInfoCacheKey] });
    },
  });
};
