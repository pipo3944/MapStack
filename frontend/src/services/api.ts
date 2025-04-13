import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// リクエストインターセプター
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// レスポンスインターセプター
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // 認証エラー (401) の場合、ログアウト処理などを行う
    if (error.response && error.response.status === 401) {
      // localStorage.removeItem('token');
      // window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// APIサービス関数
export const apiService = {
  // 認証関連
  auth: {
    login: async (email: string, password: string) => {
      const response = await apiClient.post('/auth/login', { email, password });
      return response.data;
    },
    register: async (userData: any) => {
      const response = await apiClient.post('/auth/register', userData);
      return response.data;
    },
    logout: async () => {
      const response = await apiClient.post('/auth/logout');
      return response.data;
    },
  },

  // ユーザー関連
  users: {
    getCurrentUser: async () => {
      const response = await apiClient.get('/users/me');
      return response.data;
    },
    updateProfile: async (userData: any) => {
      const response = await apiClient.patch('/users/me', userData);
      return response.data;
    },
  },

  // その他のAPIエンドポイント
};

// インターフェース定義
export interface RoadmapVersion {
  id: string;
  version: string;
  title: string;
  is_published: boolean;
  is_latest: boolean;
  published_at: string | null;
  created_at: string;
}

export interface RoadmapData {
  id: string;
  version: string;
  title: string;
  description: string | null;
  is_published: boolean;
  is_latest: boolean;
  published_at: string | null;
  created_at: string;
  theme_id: string;
}

// ロードマップのバージョン一覧を取得する
export const getRoadmapVersions = async (themeId: string): Promise<RoadmapVersion[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/themes/${themeId}/roadmaps/versions`);

    if (!response.ok) {
      throw new Error(`API呼び出しに失敗しました: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('ロードマップバージョン取得エラー:', error);
    return [];
  }
};

// 新しいロードマップバージョンを作成する
export const createNewRoadmapVersion = async (
  roadmapId: string,
  newVersion: string
): Promise<RoadmapData> => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/roadmaps/${roadmapId}/new-version?new_version=${newVersion}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      throw new Error(`API呼び出しに失敗しました: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('新しいバージョン作成エラー:', error);
    throw error;
  }
};

// ロードマップを公開する
export const publishRoadmap = async (roadmapId: string): Promise<RoadmapData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/roadmaps/${roadmapId}/publish`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`API呼び出しに失敗しました: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('ロードマップ公開エラー:', error);
    throw error;
  }
};

export default apiService;
