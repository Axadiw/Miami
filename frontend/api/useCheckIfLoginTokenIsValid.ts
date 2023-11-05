import axios from 'axios';
import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';
import { useLoginContext } from '@/contexts/LoginContext/LoginContext';

export type UseCheckIfLoginValidResult = UseQueryResult<boolean, Error>;

interface CheckIsValidTokenResponse {
  message: string;
}

export const CheckIsLoginTokenValidCacheKey = 'Is Login Token Valid';

export const checkIfLoginTokenIsValid = async (
  token: string | null | undefined
): Promise<boolean> => {
  if (!token) {
    return Promise.resolve(false);
  }

  try {
    return await axios
      .request({
        method: 'post',
        url: `${BASE_URL}/is_valid_token`,
        headers: {
          'Content-Type': 'application/json',
        },
        data: JSON.stringify({
          token,
        }),
      })
      .then((response) => response.data as CheckIsValidTokenResponse)
      .then((response) => response.message === 'Token valid')
      .catch(() => false);
  } catch (error: any) {
    throw new Error(error.response.data.error);
  }
};

export const useCheckIfLoginTokenIsValid = (): UseCheckIfLoginValidResult => {
  const { loginToken } = useLoginContext();
  return useQuery({
    queryKey: [CheckIsLoginTokenValidCacheKey, loginToken],
    queryFn: () => checkIfLoginTokenIsValid(loginToken),
    refetchInterval: 60 * 1000,
  });
};
