import axios from 'axios';
import { useMutation, UseMutationResult, useQueryClient } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';
import { useLoginContext } from '@/contexts/LoginContext/LoginContext';
import { ExchangeAccountsCacheKey } from '@/api/useListExchangeAccounts';

export type UseAddNewExchangeAccountResult = UseMutationResult<
  AddNewExchangeAccountResponse,
  Error,
  AddNewExchangeAccountProps,
  unknown
>;

export interface AddNewExchangeAccountResponse {
  message: string;
}

export interface AddNewExchangeAccountProps {
  newAccountExchangeType: string;
  newAccountName: string;
  newAccountExchangeDetails: string;
}

export async function addNewExchangeAccount(
  token: string | null | undefined,
  props: AddNewExchangeAccountProps
): Promise<AddNewExchangeAccountResponse> {
  if (!token) {
    return Promise.reject(NotLoggedInError);
  }

  return axios
    .request({
      method: 'post',
      url: `${BASE_URL}/add_new_exchange_account`,
      headers: {
        'Content-Type': 'application/json',
        'x-access-tokens': token,
      },
      data: JSON.stringify({
        type: props.newAccountExchangeType,
        name: props.newAccountName,
        details: props.newAccountExchangeDetails,
      }),
    })
    .then((response) => response.data as AddNewExchangeAccountResponse)
    .catch((error) => {
      throw new Error(error.response.data.error);
    });
}

export const useAddNewExchangeAccount = (): UseAddNewExchangeAccountResult => {
  const { loginToken } = useLoginContext();
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (props: AddNewExchangeAccountProps) => addNewExchangeAccount(loginToken, props),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [ExchangeAccountsCacheKey] });
    },
  });
};
