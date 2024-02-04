import axios from 'axios';
import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';

export interface GetTimeframesResponse {
  timeframes: string[];
}

export interface GetTimeframesProps {
  exchange: string;
}

export const TimeframesCacheKey = 'Timeframes';

export async function getTimeframes(props: GetTimeframesProps): Promise<GetTimeframesResponse> {
  return axios
    .request({
      method: 'get',
      url: `${BASE_URL}/ohlcv_timeframes?exchange=${props.exchange}`,
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then((response) => response.data as GetTimeframesResponse)
    .catch((error) => {
      throw new Error(error.response.data.error);
    });
}

export const useGetTimeframes = (
  props: GetTimeframesProps
): UseQueryResult<GetTimeframesResponse, Error> =>
  useQuery({
    queryKey: [TimeframesCacheKey, props.exchange, props],
    queryFn: () => getTimeframes(props),
  });
