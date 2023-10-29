import axios from 'axios';
import { BASE_URL } from '@/app/consts';
import { useQuery } from '@tanstack/react-query';

interface VersionResponse {
  message: string;
}

export const GetVersionCacheKey = 'GetVersionCacheKey';

async function getVersion() {
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
    });
}

export const useGetVersion = () => {
  return useQuery({
    queryKey: [GetVersionCacheKey],
    queryFn: () => getVersion(),
  });
};
