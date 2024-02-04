import axios from 'axios';
import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';

export interface GetSymbolsResponse {
  symbols: string[];
}

export interface GetSymbolsProps {
  exchange: string;
}

export const SymbolsCacheKey = 'Symbols';

export async function getSymbols(props: GetSymbolsProps): Promise<GetSymbolsResponse> {
  return axios
    .request({
      method: 'get',
      url: `${BASE_URL}/symbols?exchange=${props.exchange}`,
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then((response) => response.data as GetSymbolsResponse)
    .catch((error) => {
      throw new Error(error.response.data.error);
    });
}

export const useGetSymbols = (props: GetSymbolsProps): UseQueryResult<GetSymbolsResponse, Error> =>
  useQuery({
    queryKey: [SymbolsCacheKey, props.exchange, props],
    queryFn: () => getSymbols(props),
  });
