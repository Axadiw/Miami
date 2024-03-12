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
        twitterId: '',
        uiTimezone: '',
      };
      response.config_keys.forEach((item) => {
        switch (item.key) {
          case 'twitter_id':
            userConfig.twitterId = item.value;
            break;
          case 'ui_timezone':
            userConfig.uiTimezone = item.value;
            break;
        }
      });
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
