import axios from 'axios';
import { BASE_URL } from '@/app/consts';

interface LoginResponse {
  token: string;
}

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

export async function loginUser(login: string, password: string) {
  return axios
    .request({
      method: 'post',
      url: `${BASE_URL}/login`,
      headers: {
        'Content-Type': 'application/json',
      },
      auth: {
        username: login,
        password: password,
      },
    })
    .then((response) => {
      return response.data as LoginResponse;
    })
    .catch((error) => {
      throw new Error(error.response.data.error);
    });
}
