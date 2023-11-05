import axios from 'axios';
import { useQuery } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';

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
    .then((response) => response.data as VersionResponse)
    .then((parsedData) => parsedData.message);
}

export const useAppGetVersion = () =>
  useQuery({
    queryKey: [GetAppVersionCacheKey],
    queryFn: () => getAppVersion(),
  });
