import axios from 'axios';
import { BASE_URL } from '@/app/consts';

interface RegisterResponse {
  message: string;
}

export async function registerUser(login: string, password: string, email: string) {
  return axios
    .request({
      method: 'post',
      url: `${BASE_URL}/register`,
      headers: {
        'Content-Type': 'application/json',
      },
      data: JSON.stringify({
        username: login,
        password,
        email,
      }),
    })
    .then((response) => {
      return response.data as RegisterResponse;
    })
    .catch((error) => {
      throw new Error(error.response.data.error);
    });
}
