import { LOGIN_TOKEN_LOCAL_STORAGE_KEY } from '@/app/consts';
import { useLocalStorage } from '@mantine/hooks';

export const useLoggedIn = () => {
  const [loginToken, setLoginToken] = useLocalStorage({
    key: LOGIN_TOKEN_LOCAL_STORAGE_KEY,
  });
  return loginToken !== undefined;
};
