module.exports = {
  extends: [
    'eslint:recommended',
    'prettier',
    'mantine',
    'plugin:@next/next/recommended',
    'plugin:jest/recommended',
    'plugin:@tanstack/eslint-plugin-query/recommended',
  ],
  plugins: ['testing-library', 'jest', '@tanstack/query', 'react', 'react-hooks'],
  overrides: [
    {
      files: ['**/?(*.)+(spec|test).[jt]s?(x)'],
      extends: ['plugin:testing-library/react'],
    },
  ],
  parserOptions: {
    project: './tsconfig.json',
  },
  rules: {
    'react/react-in-jsx-scope': 'off',
    'import/extensions': 'off',
    '@tanstack/query/exhaustive-deps': 'error',
    '@tanstack/query/stable-query-client': 'error',
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'error',
  },
};
