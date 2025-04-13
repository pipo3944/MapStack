import { User } from '@/types';
import { create, StateCreator } from 'zustand';

interface UserState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // アクション
  setUser: (user: User | null) => void;
  setLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
}

const createUserStore: StateCreator<UserState> = (set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  // 同期アクション
  setUser: (user) =>
    set({
      user,
      isAuthenticated: !!user,
    }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),

  login: async (email, password) => {
    set({ isLoading: true, error: null });
    try {
      // TODO: 実際のAPIリクエストを実装
      // 仮の実装（モックデータ）
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const mockUser: User = {
        id: '1',
        name: 'テストユーザー',
        email,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      set({
        user: mockUser,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '予期せぬエラーが発生しました',
        isLoading: false,
      });
      throw error;
    }
  },

  logout: () => {
    // TODO: APIリクエストがあれば実装
    set({
      user: null,
      isAuthenticated: false,
    });
  },

  fetchUser: async () => {
    set({ isLoading: true, error: null });
    try {
      // TODO: 実際のAPIリクエストを実装
      // 仮の実装（モックデータ）
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // TODO: ログイン状態のチェック。実際はAPIでトークン検証など
      const isLoggedIn = localStorage.getItem('token') !== null;

      if (isLoggedIn) {
        const mockUser: User = {
          id: '1',
          name: 'テストユーザー',
          email: 'test@example.com',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };

        set({
          user: mockUser,
          isAuthenticated: true,
          isLoading: false,
        });
      } else {
        set({
          user: null,
          isAuthenticated: false,
          isLoading: false,
        });
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '予期せぬエラーが発生しました',
        isLoading: false,
      });
    }
  },
});

export const useUserStore = create<UserState>()(createUserStore);
