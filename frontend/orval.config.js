module.exports = {
  'mapstack-api': {
    input: {
      target: 'http://localhost:8000/api/v1/openapi.json',
    },
    output: {
      mode: 'tags-split',
      target: './src/api/generated',
      schemas: './src/api/model',
      client: 'react-query',
      override: {
        mutator: {
          path: './src/api/mutator/custom-instance.ts',
          name: 'customInstance',
        },
        operations: {
          // カテゴリ関連
          read_categories: {
            query: {
              useQuery: true,
            },
          },
          // テーマ関連
          read_themes: {
            query: {
              useQuery: true,
            },
          },
          // ロードマップ関連
          read_roadmaps: {
            query: {
              useQuery: true,
            },
          },
          read_roadmap: {
            query: {
              useQuery: true,
            },
          },
        },
      },
    },
  },
};
