import { MetadataRoute } from 'next';

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'MiamiTrade',
    short_name: 'MiamiTrade',
    description: 'MiamiTrade - risk aware trading platform',
    start_url: '/',
    display: 'standalone',
    icons: [
      {
        src: '/favicon.png',
        sizes: 'any',
        type: 'image/x-icon',
      },
    ],
  };
}
