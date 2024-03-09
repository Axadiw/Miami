import axios from 'axios';
import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';
import { useLoginContext } from '@/contexts/LoginContext/LoginContext';

export type UseListExchangeAccountsResult = UseQueryResult<ListExchangeAccountsResponse, Error>;

interface ExchangeAccount {
  id: string;
  name: string;
  type: string;
}

interface ListExchangeAccountsResponse {
  accounts: ExchangeAccount[];
}

export const ExchangeAccountsCacheKey = 'Exchange Accounts';

async function listExchangeAccounts(
  token: string | null | undefined
): Promise<ListExchangeAccountsResponse> {
  if (!token) {
    return Promise.reject(NotLoggedInError);
  }

  return (
    axios
      .request({
        method: 'get',
        url: `${BASE_URL}/list_exchange_accounts`,
        headers: {
          'Content-Type': 'application/json',
          'x-access-tokens': token,
        },
      })
      .then((response) => response.data as ListExchangeAccountsResponse)
      // .then((response) => {
      //   const userConfig: UserConfig = {
      //     email: response.email,
      //     byBitApiKey: '',
      //     byBitApiSecret: '',
      //     threeCommasAccountId: '',
      //     threeCommasApiKey: '',
      //     threeCommasSecret: '',
      //   };
      //   for (const item of response.config_keys) {
      //     switch (item.key) {
      //       case 'bybit_api_key':
      //         userConfig.byBitApiKey = item.value;
      //         break;
      //       case 'bybit_api_secret':
      //         userConfig.byBitApiSecret = item.value;
      //         break;
      //       case '3commas_account':
      //         userConfig.threeCommasAccountId = item.value;
      //         break;
      //       case '3commas_api_key':
      //         userConfig.threeCommasApiKey = item.value;
      //         break;
      //       case '3commas_secret':
      //         userConfig.threeCommasSecret = item.value;
      //         break;
      //     }
      //   }
      //   return userConfig;
      // })
      .catch((error) => {
        throw new Error(error.response.data.error);
      })
  );
}

export const useListExchangeAccounts = (): UseListExchangeAccountsResult => {
  const { loginToken } = useLoginContext();
  return useQuery({
    queryKey: [ExchangeAccountsCacheKey, loginToken],
    queryFn: () => listExchangeAccounts(loginToken),
  });
};
