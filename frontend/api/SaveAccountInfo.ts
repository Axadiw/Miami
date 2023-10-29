import axios from 'axios';
import { BASE_URL } from '@/app/consts';
import { UserConfig } from '@/app/account/accountPage';

export async function saveAccountInfo(token: string, info: UserConfig) {
  return axios
    .request({
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
    })

    .catch((error) => {
      throw new Error(error.response.data.error);
    });
}
