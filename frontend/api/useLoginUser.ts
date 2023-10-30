import axios from 'axios';
import { BASE_URL } from '@/app/consts';
import { useMutation } from '@tanstack/react-query';

interface LoginResponse {
  token: string;
}

export interface LoginProps {
  login: string;
  password: string;
}

export async function loginUser(props: LoginProps) {
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
    .then((response) => {
      return response.data as LoginResponse;
    })
    .catch((error) => {
      throw new Error(error.response.data.error);
    });
}

export const useLoginUser = () => {
  return useMutation({
    mutationFn: (props: LoginProps) => {
      return loginUser(props);
    },
  });
};
