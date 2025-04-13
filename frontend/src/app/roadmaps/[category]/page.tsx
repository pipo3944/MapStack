'use client';

import {
  useReadCategoryApiV1CategoriesCategoryIdGet,
  useReadThemesApiV1ThemesGet,
} from '@/api/generated/roadmap/roadmap';
import { CategoryResponse, ThemeResponse } from '@/api/model';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function CategoryPage() {
  const params = useParams();
  const router = useRouter();
  const categoryId = params?.category as string;

  // カテゴリ詳細を取得
  const {
    data: categoryData,
    isLoading: isLoadingCategory,
    error: categoryError,
  } = useReadCategoryApiV1CategoriesCategoryIdGet(categoryId);

  // そのカテゴリに紐づくテーマ一覧を取得
  const {
    data: themesData,
    isLoading: isLoadingThemes,
    error: themesError,
  } = useReadThemesApiV1ThemesGet(
    { category_id: categoryId },
    {
      query: {
        enabled: !!categoryId,
      },
    }
  );

  const [category, setCategory] = useState<CategoryResponse | null>(null);
  const [themes, setThemes] = useState<ThemeResponse[]>([]);

  // カテゴリデータが取得できたら状態を更新
  useEffect(() => {
    if (categoryData?.success && categoryData.data) {
      setCategory(categoryData.data);
    }
  }, [categoryData]);

  // テーマデータが取得できたら状態を更新
  useEffect(() => {
    if (themesData?.success && themesData.data) {
      setThemes(themesData.data);
    }
  }, [themesData]);

  // ローディング中の表示
  if (isLoadingCategory || isLoadingThemes) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4">データを読み込み中...</p>
      </div>
    );
  }

  // エラーの表示
  if (categoryError || themesError || !categoryData?.success) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <h1 className="text-3xl font-bold mb-8 text-red-500">エラーが発生しました</h1>
        <p className="text-gray-600 mb-4">
          データの取得中に問題が発生しました。後でもう一度お試しください。
        </p>
        <div className="flex justify-center gap-4">
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            再読み込み
          </button>
          <Link href="/roadmaps">
            <span className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded inline-block">
              カテゴリ一覧に戻る
            </span>
          </Link>
        </div>
      </div>
    );
  }

  // カテゴリが見つからない場合
  if (!category) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <h1 className="text-3xl font-bold mb-8 text-yellow-500">カテゴリが見つかりません</h1>
        <p className="text-gray-600 mb-4">
          指定されたカテゴリは存在しないか、削除された可能性があります。
        </p>
        <Link href="/roadmaps">
          <span className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            カテゴリ一覧に戻る
          </span>
        </Link>
      </div>
    );
  }

  const handleThemeClick = (themeId: string) => {
    router.push(`/roadmaps/${categoryId}/${themeId}`);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <Link href="/roadmaps">
          <span className="text-blue-600 hover:underline">← カテゴリ一覧に戻る</span>
        </Link>
      </div>

      <h1 className="text-3xl font-bold mb-4">{category.title}</h1>
      <p className="text-gray-600 mb-8">{category.description || ''}</p>

      {themes.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-xl text-gray-500">このカテゴリにはテーマがまだありません</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {themes.map((theme) => (
            <div
              key={theme.id}
              className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
              onClick={() => handleThemeClick(theme.id)}
            >
              <div className="h-40 bg-gray-300 flex items-center justify-center">
                <span className="text-4xl text-gray-600 font-medium">
                  {theme.title.substring(0, 1)}
                </span>
              </div>
              <div className="p-4">
                <h2 className="text-xl font-semibold mb-2">{theme.title}</h2>
                <p className="text-gray-600">{theme.description || '説明はありません'}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
