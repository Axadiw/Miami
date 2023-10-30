import axios from 'axios';
import { BASE_URL } from '@/app/consts';
import { useMutation } from '@tanstack/react-query';

interface RegisterResponse {
  message: string;
}

export interface RegisterProps {
  login: string;
  password: string;
  email: string;
}

const registerUser = async (props: RegisterProps) => {
  try {
    let response = await axios.request({
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

export const useRegisterUser = () => {
  return useMutation({
    mutationFn: (props: RegisterProps) => {
      return registerUser(props);
    },
  });
};
