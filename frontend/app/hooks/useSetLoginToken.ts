import { LOGIN_TOKEN_LOCAL_STORAGE_KEY } from '@/app/consts';
import { useLocalStorage } from '@mantine/hooks';
import { useCallback } from 'react';

export const useSetLoginToken = () => {
  const [_, setLoginToken, removeValue] = useLocalStorage({
    key: LOGIN_TOKEN_LOCAL_STORAGE_KEY,
  });
  return useCallback((newValue: string | undefined) => {
    if (newValue) {
      setLoginToken(newValue);
    } else {
      removeValue();
    }
  }, []);
};
