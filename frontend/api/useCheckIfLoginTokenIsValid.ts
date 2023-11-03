import axios from 'axios';
import { BASE_URL } from '@/app/consts';

interface IsValidTokenResponse {
  message: string;
}

export const IsLoginTokenValidCacheKey = 'Is Login Token Valid';

export const checkIfLoginTokenIsValid = async (token: string | null | undefined) => {
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
      .then((response) => response.data as IsValidTokenResponse)
      .then((response) => response.message === 'Token valid')
      .catch(() => false);
  } catch (error: any) {
    throw new Error(error.response.data.error);
  }
};
