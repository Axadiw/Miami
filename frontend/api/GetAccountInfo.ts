import axios from 'axios';
import { BASE_URL } from '@/app/consts';
import { UserConfig } from '@/app/account/accountPage';

interface ConfigPair {
  key: string;
  value: string;
}

interface AccountInfoResponse {
  config_keys: ConfigPair[];
  email: string;
}

export async function getAccountInfo(token: string) {
  return axios
    .request({
      method: 'get',
      url: `${BASE_URL}/account_info`,
      headers: {
        'Content-Type': 'application/json',
        'x-access-tokens': token,
      },
    })
    .then((response) => {
      return response.data as AccountInfoResponse;
    })
    .then((response) => {
      const userConfig: UserConfig = {
        email: response.email,
        byBitApiKey: '',
        byBitApiSecret: '',
        threeCommasAccountId: '',
        threeCommasApiKey: '',
        threeCommasSecret: '',
      };
      for (let item of response.config_keys) {
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
