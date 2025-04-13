'use client';

import { useReadCategoriesApiV1CategoriesGet } from '@/api/generated/roadmap/roadmap';
import { CategoryResponse } from '@/api/model';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function CategoriesPage() {
  const router = useRouter();
  const { data, isLoading, error } = useReadCategoriesApiV1CategoriesGet();
  const [categories, setCategories] = useState<CategoryResponse[]>([]);

  useEffect(() => {
    if (data?.success && data.data) {
      setCategories(data.data);
    }
  }, [data]);

  const handleCategoryClick = (categoryId: string) => {
    router.push(`/roadmaps/${categoryId}`);
  };

  // ローディング中の表示
  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <div className="animate-pulse">
          <h1 className="text-3xl font-bold mb-8">学習カテゴリを読み込み中...</h1>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-gray-200 rounded-lg h-64"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // エラーの表示
  if (error || !data?.success) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <h1 className="text-3xl font-bold mb-8 text-red-500">エラーが発生しました</h1>
        <p className="text-gray-600 mb-4">
          カテゴリ情報の取得中に問題が発生しました。後でもう一度お試しください。
        </p>
        <button
          onClick={() => window.location.reload()}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          再読み込み
        </button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-center">学習カテゴリ</h1>
      <p className="text-gray-600 text-center mb-12">
        興味のある分野を選んで、専門的なロードマップを見つけましょう
      </p>

      {categories.length === 0 ? (
        <p className="text-center text-gray-500">カテゴリが見つかりませんでした</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {categories.map((category) => (
            <div
              key={category.id}
              className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
              onClick={() => handleCategoryClick(category.id)}
            >
              <div className="h-40 bg-gray-200">
                {/* 画像フィールドがAPIから提供されていない場合は、プレースホルダー表示 */}
                <div className="w-full h-full bg-gray-300 flex items-center justify-center">
                  <span className="text-gray-600 font-medium">
                    {category.title.substring(0, 1)}
                  </span>
                </div>
              </div>
              <div className="p-4">
                <h2 className="text-xl font-semibold mb-2">{category.title}</h2>
                <p className="text-gray-600">{category.description || '説明はありません'}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
