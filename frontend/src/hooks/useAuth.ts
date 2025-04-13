import apiService from '@/services/api';
import { useUserStore } from '@/store/userStore';
import { useRouter } from 'next/navigation';
import { useCallback } from 'react';

export const useAuth = () => {
  const router = useRouter();
  const { user, isLoading, isAuthenticated, setUser, setLoading, setError } = useUserStore();

  const login = useCallback(
    async (email: string, password: string) => {
      setLoading(true);
      try {
        const response = await apiService.auth.login(email, password);

        // トークンをローカルストレージに保存
        if (response.token) {
          localStorage.setItem('token', response.token);
        }

        // ユーザー情報を取得して保存
        const userData = await apiService.users.getCurrentUser();
        setUser(userData);

        return userData;
      } catch (error) {
        setError(error instanceof Error ? error.message : '認証に失敗しました');
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [setLoading, setUser, setError]
  );

  const logout = useCallback(async () => {
    setLoading(true);
    try {
      await apiService.auth.logout();
    } catch (error) {
      // エラーが発生しても続行（ログアウト処理は続行する）
      console.error('Logout error:', error);
    } finally {
      // ローカルストレージからトークンを削除
      localStorage.removeItem('token');
      // ユーザー情報をクリア
      setUser(null);
      setLoading(false);
      // ログインページにリダイレクト
      router.push('/login');
    }
  }, [router, setLoading, setUser]);

  const checkAuthStatus = useCallback(async () => {
    // すでに認証済みの場合はスキップ
    if (isAuthenticated && user) return user;

    const token = localStorage.getItem('token');
    if (!token) return null;

    setLoading(true);
    try {
      const userData = await apiService.users.getCurrentUser();
      setUser(userData);
      return userData;
    } catch (error) {
      // 認証エラーの場合はトークンを削除
      localStorage.removeItem('token');
      setUser(null);
      return null;
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated, user, setLoading, setUser]);

  return {
    user,
    isLoading,
    isAuthenticated,
    login,
    logout,
    checkAuthStatus,
  };
};

export default useAuth;
