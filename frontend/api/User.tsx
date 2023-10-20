import axios from 'axios';

export let BASE_URL = 'https://api.miamitrade.pro';

if (process.env.NODE_ENV === 'development') {
  BASE_URL = 'http://localhost:5000';
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
      console.log(JSON.stringify(response.data));
    })
    .catch((error) => {
      console.log(error);
    });
}
