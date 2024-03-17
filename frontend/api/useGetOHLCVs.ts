import axios from 'axios';
import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';
import { Time } from '@/vendor/lightweight-charts/src/model/horz-scale-behavior-time/types';

export interface OHLCV {
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  time: Time;
}

export interface GetOHLCVsResponse {
  ohlcvs: OHLCV[];
}

export interface GetOHLCVsProps {
  exchange: string;
  timeframe: string;
  symbol: string;
  limit: number | undefined;
}

export const OHLCVsCacheKey = 'OHLCVs';

export async function getOHLCVs(props: GetOHLCVsProps): Promise<GetOHLCVsResponse> {
  return axios
    .request({
      method: 'get',
      url: `${BASE_URL}/ohlcv?exchange=${props.exchange}&tf=${props.timeframe}&symbol=${props.symbol}&limit=${props.limit}`,
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then((response) => response.data as GetOHLCVsResponse)
    .catch((error) => {
      throw new Error(error.response.data.error);
    });
}

export const useGetOHLCVs = (props: GetOHLCVsProps): UseQueryResult<GetOHLCVsResponse, Error> =>
  useQuery({
    queryKey: [OHLCVsCacheKey, props.exchange, props.symbol, props.timeframe, props.limit, props],
    queryFn: () => getOHLCVs(props),
    enabled: props.limit !== undefined && props.symbol !== '' && props.timeframe !== '',
  });
