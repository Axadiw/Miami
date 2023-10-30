import axios from 'axios';
import { BASE_URL } from '@/app/consts';
import { useQuery } from '@tanstack/react-query';

interface VersionResponse {
  message: string;
}

export const GetAppVersionCacheKey = 'App version';

async function getAppVersion() {
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

export const useAppGetVersion = () => {
  return useQuery({
    queryKey: [GetAppVersionCacheKey],
    queryFn: () => getAppVersion(),
  });
};
