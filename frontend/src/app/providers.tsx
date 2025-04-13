'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState, type ReactNode } from 'react';

interface ProvidersProps {
  children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  // クライアントコンポーネントでクエリクライアントをステートとして保持
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            // デフォルトのキャッシュ時間と再試行設定
            staleTime: 60 * 1000, // 1分間はデータをstaleとみなさない
            gcTime: 5 * 60 * 1000, // 5分間はキャッシュを保持
            retry: 1, // エラー時に1回だけ再試行
            refetchOnWindowFocus: false, // ウィンドウフォーカス時に再取得しない
          },
        },
      })
  );

  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
}
