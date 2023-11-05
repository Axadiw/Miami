import axios from 'axios';
import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';

export type UseGetAppVersionResult = UseQueryResult<string, Error>;

interface VersionResponse {
  message: string;
}

export const GetAppVersionCacheKey = 'App version';

async function getAppVersion(): Promise<string> {
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

export const useAppGetVersion = (): UseGetAppVersionResult =>
  useQuery({
    queryKey: [GetAppVersionCacheKey],
    queryFn: () => getAppVersion(),
  });
