/**
 * カスタムHTTPクライアント
 *
 * API通信用のカスタムAxiosインスタンスを提供します。
 * - 認証トークンの自動付与
 * - エラーハンドリング
 * - API URLの環境変数対応
 */
import axios, { AxiosError, AxiosRequestConfig } from 'axios';

// APIベースURL（環境変数から取得、デフォルトはローカル開発環境のURL）
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * カスタムAxiosインスタンスを提供するmutator関数
 * orvalの設定ファイルで指定して使用します
 */
export const customInstance = <T>(config: AxiosRequestConfig): Promise<T> => {
  const source = axios.CancelToken.source();
  const instance = axios.create({
    baseURL: API_URL,
    timeout: 10000,
    cancelToken: source.token,
  });

  // リクエストインターセプター
  instance.interceptors.request.use(
    (config) => {
      // クライアントサイドの場合のみトークンを取得・設定
      if (typeof window !== 'undefined') {
        const token = localStorage.getItem('auth_token');
        if (token) {
          // headers を安全に更新
          config.headers = config.headers || {};
          config.headers['Authorization'] = `Bearer ${token}`;
        }
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // レスポンスインターセプター
  instance.interceptors.response.use(
    (response) => {
      // 正常レスポンスの場合はdataプロパティを返す
      return response.data;
    },
    (error: AxiosError) => {
      // エラーレスポンスのハンドリング
      if (error.response?.status === 401) {
        // 認証エラーの場合はログアウト処理などを実行
        if (typeof window !== 'undefined') {
          // localStorage.removeItem('auth_token');
          // リダイレクト処理など
          console.error('認証エラーが発生しました。再ログインが必要です。');
        }
      }

      // エラーオブジェクトのカスタマイズ
      const errorObj = {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        message: error.message,
      };

      console.error('API Error:', errorObj);
      return Promise.reject(errorObj);
    }
  );

  return instance(config) as Promise<T>;
};
