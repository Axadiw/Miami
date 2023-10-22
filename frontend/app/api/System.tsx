import axios from 'axios';
import { BASE_URL } from '@/app/api/consts';

interface VersionResponse {
  message: string;
}

export async function getVersion() {
  return axios
    .request({
      method: 'get',
      url: `${BASE_URL}/version`,
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then((response) => {
      return response.data as VersionResponse;
    })
    .then((parsedData) => {
      return parsedData.message;
    })
    .catch((error) => {
      console.log(error);
    });
}
