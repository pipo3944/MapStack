'use client';

import useAuth from '@/hooks/useAuth';

export default function Header() {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <a href="/" className="text-2xl font-bold text-blue-600">
          MapStack
        </a>
        <nav>
          <ul className="flex space-x-6">
            <li>
              <a href="/roadmaps" className="hover:text-blue-600 transition-colors">
                ロードマップ
              </a>
            </li>
            <li>
              <a href="/practice" className="hover:text-blue-600 transition-colors">
                実践演習
              </a>
            </li>
            <li>
              <a href="/ai-assistant" className="hover:text-blue-600 transition-colors">
                AIアシスタント
              </a>
            </li>
            {isAuthenticated && (
              <li>
                <a href="/profile" className="hover:text-blue-600 transition-colors">
                  プロフィール
                </a>
              </li>
            )}
          </ul>
        </nav>
        <div>
          {isAuthenticated ? (
            <div className="flex items-center">
              <span className="mr-4">{user?.name}</span>
              <button
                onClick={() => logout()}
                className="px-4 py-2 rounded hover:bg-gray-100 transition-colors"
              >
                ログアウト
              </button>
            </div>
          ) : (
            <>
              <a href="/login" className="px-4 py-2 rounded hover:bg-gray-100 transition-colors">
                ログイン
              </a>
              <a
                href="/signup"
                className="ml-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
              >
                新規登録
              </a>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
