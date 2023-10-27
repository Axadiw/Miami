import axios from 'axios';
import { BASE_URL } from '@/app/consts';
import { UserConfig } from '@/app/account/accountPage';

interface LoginResponse {
  token: string;
}

interface RegisterResponse {
  message: string;
}

interface ConfigPair {
  key: string;
  value: string;
}

interface AccountInfoResponse {
  config_keys: ConfigPair[];
  email: string;
}

export async function registerUser(login: string, password: string, email: string) {
  return axios
    .request({
      method: 'post',
      url: `${BASE_URL}/register`,
      headers: {
        'Content-Type': 'application/json',
      },
      data: JSON.stringify({
        username: login,
        password,
        email,
      }),
    })
    .then((response) => {
      return response.data as RegisterResponse;
    })
    .catch((error) => {
      throw new Error(error.response.data.error);
    });
}

export async function loginUser(login: string, password: string) {
  return axios
    .request({
      method: 'post',
      url: `${BASE_URL}/login`,
      headers: {
        'Content-Type': 'application/json',
      },
      auth: {
        username: login,
        password: password,
      },
    })
    .then((response) => {
      return response.data as LoginResponse;
    })
    .catch((error) => {
      throw new Error(error.response.data.error);
    });
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
