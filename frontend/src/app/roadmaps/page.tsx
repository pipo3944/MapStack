'use client';

import { useRouter } from 'next/navigation';

// カテゴリデータ（実際のアプリケーションではAPIから取得することが望ましい）
const categories = [
  {
    id: 'web-development',
    title: 'Web開発',
    description: 'フロントエンド、バックエンド、DevOpsなどのWeb開発に関連するスキルマップ',
    image: '/images/categories/web-development.jpg',
  },
  {
    id: 'data-science',
    title: 'データサイエンス',
    description: 'データ分析、機械学習、AIなどデータを活用するためのスキルマップ',
    image: '/images/categories/data-science.jpg',
  },
  {
    id: 'mobile-development',
    title: 'モバイル開発',
    description: 'iOS、Android、クロスプラットフォームなどのモバイルアプリ開発のスキルマップ',
    image: '/images/categories/mobile-development.jpg',
  },
  {
    id: 'infrastructure',
    title: 'インフラストラクチャ',
    description: 'クラウド、ネットワーク、サーバー管理などのインフラ関連のスキルマップ',
    image: '/images/categories/infrastructure.jpg',
  },
];

export default function CategoriesPage() {
  const router = useRouter();

  const handleCategoryClick = (categoryId: string) => {
    router.push(`/roadmaps/${categoryId}`);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-center">学習カテゴリ</h1>
      <p className="text-gray-600 text-center mb-12">
        興味のある分野を選んで、専門的なロードマップを見つけましょう
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {categories.map((category) => (
          <div
            key={category.id}
            className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
            onClick={() => handleCategoryClick(category.id)}
          >
            <div className="h-40 bg-gray-200">
              {/* 画像がない場合はグレーのプレースホルダー表示 */}
              {category.image && (
                <img
                  src={category.image}
                  alt={category.title}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.currentTarget.style.display = 'none';
                  }}
                />
              )}
            </div>
            <div className="p-4">
              <h2 className="text-xl font-semibold mb-2">{category.title}</h2>
              <p className="text-gray-600">{category.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
