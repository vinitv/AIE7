/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  // Remove rewrites since API and frontend are served from same domain
  env: {
    API_URL: process.env.API_URL || '',
  },
};

module.exports = nextConfig; 