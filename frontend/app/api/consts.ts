export let BASE_URL = 'https://api.miamitrade.pro';

if (process.env.NODE_ENV === 'development') {
  BASE_URL = 'http://localhost:5000';
}
