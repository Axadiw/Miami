// eslint-disable-next-line import/no-mutable-exports
export let BASE_URL = 'https://api.miamitrade.pro';

if (process.env.NODE_ENV === 'development') {
  BASE_URL = 'http://localhost:5000';
}

export const LOGIN_TOKEN_LOCAL_STORAGE_KEY = 'LOGIN_TOKEN_LOCAL_STORAGE_KEY';
