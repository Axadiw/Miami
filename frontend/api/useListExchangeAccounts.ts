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

  return axios
    .request({
      method: 'get',
      url: `${BASE_URL}/list_exchange_accounts`,
      headers: {
        'Content-Type': 'application/json',
        'x-access-tokens': token,
      },
    })
    .then((response) => response.data as ListExchangeAccountsResponse)
    .catch((error) => {
      throw new Error(error.response.data.error);
    });
}

export const useListExchangeAccounts = (): UseListExchangeAccountsResult => {
  const { loginToken } = useLoginContext();
  return useQuery({
    queryKey: [ExchangeAccountsCacheKey, loginToken],
    queryFn: () => listExchangeAccounts(loginToken),
  });
};
