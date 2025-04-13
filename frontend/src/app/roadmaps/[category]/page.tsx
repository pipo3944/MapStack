'use client';

import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

// カテゴリとテーマのデータ定義
interface Theme {
  id: string;
  title: string;
  description: string;
  image?: string;
}

interface Category {
  id: string;
  title: string;
  description: string;
  themes: Theme[];
}

// カテゴリデータ（本来はAPIから取得するべき）
const categoryData: Record<string, Category> = {
  'web-development': {
    id: 'web-development',
    title: 'Web開発',
    description: 'フロントエンド、バックエンド、DevOpsなどのWeb開発に関連するスキルマップ',
    themes: [
      {
        id: 'frontend',
        title: 'フロントエンド開発',
        description: 'HTML、CSS、JavaScriptからモダンフレームワークまでのフロントエンド技術',
        image: '/images/themes/frontend.jpg',
      },
      {
        id: 'backend',
        title: 'バックエンド開発',
        description: 'サーバーサイド開発、API設計、データベース連携などのバックエンド技術',
        image: '/images/themes/backend.jpg',
      },
      {
        id: 'fullstack',
        title: 'フルスタック開発',
        description: 'フロントエンドとバックエンドの両方を扱うフルスタック開発者になるためのパス',
        image: '/images/themes/fullstack.jpg',
      },
      {
        id: 'devops',
        title: 'DevOps',
        description: '継続的インテグレーション、デリバリー、デプロイメントのための自動化とツール',
        image: '/images/themes/devops.jpg',
      },
    ],
  },
  'data-science': {
    id: 'data-science',
    title: 'データサイエンス',
    description: 'データ分析、機械学習、AIなどデータを活用するためのスキルマップ',
    themes: [
      {
        id: 'data-analysis',
        title: 'データ分析',
        description: 'データの収集、クリーニング、分析、可視化の基礎スキル',
        image: '/images/themes/data-analysis.jpg',
      },
      {
        id: 'machine-learning',
        title: '機械学習',
        description: '機械学習アルゴリズム、モデル構築、評価手法の習得',
        image: '/images/themes/machine-learning.jpg',
      },
      {
        id: 'big-data',
        title: 'ビッグデータ',
        description: '大規模データの処理、分散処理フレームワークの活用',
        image: '/images/themes/big-data.jpg',
      },
      {
        id: 'deep-learning',
        title: 'ディープラーニング',
        description: 'ニューラルネットワーク、ディープラーニングモデルの構築と応用',
        image: '/images/themes/deep-learning.jpg',
      },
    ],
  },
  'mobile-development': {
    id: 'mobile-development',
    title: 'モバイル開発',
    description: 'iOS、Android、クロスプラットフォームなどのモバイルアプリ開発のスキルマップ',
    themes: [
      {
        id: 'ios',
        title: 'iOS開発',
        description: 'Swift、UIKitを使ったiOSアプリケーション開発',
        image: '/images/themes/ios.jpg',
      },
      {
        id: 'android',
        title: 'Android開発',
        description: 'KotlinやJavaを使ったAndroidアプリケーション開発',
        image: '/images/themes/android.jpg',
      },
      {
        id: 'react-native',
        title: 'React Native',
        description: 'JavaScriptを使ったクロスプラットフォームモバイルアプリ開発',
        image: '/images/themes/react-native.jpg',
      },
      {
        id: 'flutter',
        title: 'Flutter',
        description: 'Dartを使ったクロスプラットフォームモバイルアプリ開発',
        image: '/images/themes/flutter.jpg',
      },
    ],
  },
  infrastructure: {
    id: 'infrastructure',
    title: 'インフラストラクチャ',
    description: 'クラウド、ネットワーク、サーバー管理などのインフラ関連のスキルマップ',
    themes: [
      {
        id: 'cloud',
        title: 'クラウドコンピューティング',
        description: 'AWS、Azure、GCPなどのクラウドプラットフォーム活用スキル',
        image: '/images/themes/cloud.jpg',
      },
      {
        id: 'networking',
        title: 'ネットワーキング',
        description: 'ネットワークの基礎、設計、セキュリティ、トラブルシューティング',
        image: '/images/themes/networking.jpg',
      },
      {
        id: 'server-admin',
        title: 'サーバー管理',
        description: 'Linux/Windowsサーバーの構築、管理、最適化',
        image: '/images/themes/server-admin.jpg',
      },
      {
        id: 'containerization',
        title: 'コンテナ技術',
        description: 'Docker、Kubernetes、コンテナオーケストレーション',
        image: '/images/themes/containerization.jpg',
      },
    ],
  },
};

export default function CategoryPage() {
  const params = useParams();
  const router = useRouter();
  const categoryId = params?.category as string;
  const [category, setCategory] = useState<Category | null>(null);

  useEffect(() => {
    // カテゴリIDからカテゴリデータを取得
    if (categoryId && categoryData[categoryId]) {
      setCategory(categoryData[categoryId]);
    } else {
      // 無効なカテゴリの場合はカテゴリ一覧ページにリダイレクト
      router.push('/roadmaps');
    }
  }, [categoryId, router]);

  if (!category) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4">カテゴリを読み込み中...</p>
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
      <p className="text-gray-600 mb-8">{category.description}</p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {category.themes.map((theme) => (
          <div
            key={theme.id}
            className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
            onClick={() => handleThemeClick(theme.id)}
          >
            <div className="h-40 bg-gray-200">
              {theme.image && (
                <img
                  src={theme.image}
                  alt={theme.title}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.currentTarget.style.display = 'none';
                  }}
                />
              )}
            </div>
            <div className="p-4">
              <h2 className="text-xl font-semibold mb-2">{theme.title}</h2>
              <p className="text-gray-600">{theme.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
