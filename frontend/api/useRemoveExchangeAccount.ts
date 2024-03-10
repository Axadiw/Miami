import axios from 'axios';
import { useMutation, UseMutationResult, useQueryClient } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';
import { useLoginContext } from '@/contexts/LoginContext/LoginContext';
import { ExchangeAccountsCacheKey } from '@/api/useListExchangeAccounts';

export type UseRemoveExchangeAccountResult = UseMutationResult<
  RemoveExchangeAccountResponse,
  Error,
  RemoveExchangeAccountProps,
  unknown
>;

export interface RemoveExchangeAccountResponse {
  message: string;
}

export interface RemoveExchangeAccountProps {
  accountId: string;
}

export async function removeExchangeAccount(
  token: string | null | undefined,
  props: RemoveExchangeAccountProps
): Promise<RemoveExchangeAccountResponse> {
  if (!token) {
    return Promise.reject(NotLoggedInError);
  }

  return axios
    .request({
      method: 'post',
      url: `${BASE_URL}/remove_exchange_account`,
      headers: {
        'Content-Type': 'application/json',
        'x-access-tokens': token,
      },
      data: JSON.stringify({
        id: props.accountId,
      }),
    })
    .then((response) => response.data as RemoveExchangeAccountResponse)
    .catch((error) => {
      throw new Error(error.response.data.error);
    });
}

export const useRemoveExchangeAccount = (): UseRemoveExchangeAccountResult => {
  const { loginToken } = useLoginContext();
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (props: RemoveExchangeAccountProps) => removeExchangeAccount(loginToken, props),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [ExchangeAccountsCacheKey] });
    },
  });
};
