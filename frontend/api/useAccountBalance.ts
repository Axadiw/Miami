import axios from 'axios';
import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';
import { useLoginContext } from '@/contexts/LoginContext/LoginContext';

export interface GetAccountBalanceResponse {
  balance: number;
}

export interface GetAccountBalanceProps {
  accountId: string | undefined;
  token?: string | null | undefined;
}

export const AccountBalanceCacheKey = 'AccountBalance';

export async function getAccountBalance(
  props: GetAccountBalanceProps
): Promise<GetAccountBalanceResponse> {
  if (!props.token) {
    return Promise.reject(NotLoggedInError);
  }

  return axios
    .request({
      method: 'get',
      url: `${BASE_URL}/exchange_get_balance?account=${props.accountId}`,
      headers: {
        'Content-Type': 'application/json',
        'x-access-tokens': props.token,
      },
    })
    .then((response) => response.data as GetAccountBalanceResponse)
    .catch((error) => {
      throw new Error(error.response.data.error);
    });
}

export const useGetAccountBalance = (
  props: GetAccountBalanceProps
): UseQueryResult<GetAccountBalanceResponse, Error> => {
  const { loginToken } = useLoginContext();
  return useQuery({
    queryKey: [AccountBalanceCacheKey, props.accountId, loginToken, props],
    queryFn: () => getAccountBalance({ ...props, token: loginToken }),
    enabled: props.accountId !== undefined,
  });
};
