import axios from 'axios';
import { useMutation, UseMutationResult } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';

export type UseRegisterUserResult = UseMutationResult<
  RegisterResponse,
  Error,
  RegisterProps,
  unknown
>;

export interface RegisterResponse {
  message: string;
}

export interface RegisterProps {
  login: string;
  password: string;
  email: string;
}

const registerUser = async (props: RegisterProps): Promise<RegisterResponse> => {
  try {
    const response = await axios.request({
      method: 'post',
      url: `${BASE_URL}/register`,
      headers: {
        'Content-Type': 'application/json',
      },
      data: JSON.stringify({
        username: props.login,
        password: props.password,
        email: props.email,
      }),
    });
    return response.data as RegisterResponse;
  } catch (error: any) {
    throw new Error(error.response.data.error);
  }
};

export const useRegisterUser = (): UseRegisterUserResult =>
  useMutation({
    mutationFn: (props: RegisterProps) => registerUser(props),
  });
