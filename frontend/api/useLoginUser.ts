import axios from 'axios';
import { useMutation, UseMutationResult } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';

export type UseLoginUserResult = UseMutationResult<LoginResponse, Error, LoginProps, unknown>;

export interface LoginResponse {
  token: string;
}

export interface LoginProps {
  login: string;
  password: string;
}

export async function loginUser(props: LoginProps): Promise<LoginResponse> {
  return axios
    .request({
      method: 'post',
      url: `${BASE_URL}/login`,
      headers: {
        'Content-Type': 'application/json',
      },
      auth: {
        username: props.login,
        password: props.password,
      },
    })
    .then((response) => response.data as LoginResponse)
    .catch((error) => {
      throw new Error(error.response.data.error);
    });
}

export const useLoginUser = (): UseLoginUserResult =>
  useMutation({
    mutationFn: (props: LoginProps) => loginUser(props),
  });
