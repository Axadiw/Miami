import axios from 'axios';
import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';
import { useLoginContext } from '@/contexts/LoginContext/LoginContext';
import { UserConfig } from '@/app/account/components/userConfig/userConfigTab';

export type UseGetAccountInfoResult = UseQueryResult<UserConfig, Error>;

interface ConfigPair {
  key: string;
  value: string;
}

interface AccountInfoResponse {
  config_keys: ConfigPair[];
  email: string;
}

export const AccountInfoCacheKey = 'Account info';

async function getAccountInfo(token: string | null | undefined): Promise<UserConfig> {
  if (!token) {
    return Promise.reject(NotLoggedInError);
  }

  return axios
    .request({
      method: 'get',
      url: `${BASE_URL}/account_info`,
      headers: {
        'Content-Type': 'application/json',
        'x-access-tokens': token,
      },
    })
    .then((response) => response.data as AccountInfoResponse)
    .then((response) => {
      const userConfig: UserConfig = {
        email: response.email,
        byBitApiKey: '',
        byBitApiSecret: '',
        threeCommasAccountId: '',
        threeCommasApiKey: '',
        threeCommasSecret: '',
      };
      for (const item of response.config_keys) {
        switch (item.key) {
          case 'bybit_api_key':
            userConfig.byBitApiKey = item.value;
            break;
          case 'bybit_api_secret':
            userConfig.byBitApiSecret = item.value;
            break;
          case '3commas_account':
            userConfig.threeCommasAccountId = item.value;
            break;
          case '3commas_api_key':
            userConfig.threeCommasApiKey = item.value;
            break;
          case '3commas_secret':
            userConfig.threeCommasSecret = item.value;
            break;
        }
      }
      return userConfig;
    })
    .catch((error) => {
      throw new Error(error.response.data.error);
    });
}

export const useGetAccountInfo = (): UseGetAccountInfoResult => {
  const { loginToken } = useLoginContext();
  return useQuery({
    queryKey: [AccountInfoCacheKey, loginToken],
    queryFn: () => getAccountInfo(loginToken),
  });
};
