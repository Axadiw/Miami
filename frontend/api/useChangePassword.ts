import axios from 'axios';
import { useMutation, UseMutationResult } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';
import { useLoginContext } from '@/contexts/LoginContext/LoginContext';

export type UseChangePasswordResult = UseMutationResult<
  ChangePasswordResponse,
  Error,
  ChangePasswordProps,
  unknown
>;

export interface ChangePasswordResponse {
  message: string;
}

export interface ChangePasswordProps {
  oldPassword: string;
  newPassword: string;
}

const changePassword = async (
  token: string | null | undefined,
  props: ChangePasswordProps
): Promise<ChangePasswordResponse> => {
  if (!token) {
    return Promise.reject(NotLoggedInError);
  }

  try {
    const response = await axios.request({
      method: 'post',
      url: `${BASE_URL}/change_password`,
      headers: {
        'Content-Type': 'application/json',
        'x-access-tokens': token,
      },
      data: JSON.stringify({
        old_password: props.oldPassword,
        new_password: props.newPassword,
      }),
    });
    return response.data as ChangePasswordResponse;
  } catch (error: any) {
    throw new Error(error.response.data.error);
  }
};

export const useChangePassword = (): UseChangePasswordResult => {
  const { loginToken } = useLoginContext();
  return useMutation({
    mutationFn: (props: ChangePasswordProps) => changePassword(loginToken, props),
  });
};
