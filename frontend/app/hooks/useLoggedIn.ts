import { LOGIN_TOKEN_LOCAL_STORAGE_KEY } from '@/app/consts';
import { useLocalStorage } from '@mantine/hooks';

export const useLoggedIn = () => {
  const [loginToken, _] = useLocalStorage({
    key: LOGIN_TOKEN_LOCAL_STORAGE_KEY,
    defaultValue:
      typeof localStorage !== 'undefined'
        ? localStorage.getItem(LOGIN_TOKEN_LOCAL_STORAGE_KEY)
        : undefined,
  });
  return loginToken !== undefined && loginToken !== null;
};
