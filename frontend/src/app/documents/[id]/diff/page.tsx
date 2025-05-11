'use client';

import { DiffViewer } from '@/components/document';
import { useDocuments } from '@/hooks';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect } from 'react';

interface DiffPageProps {
  params: {
    id: string;
  };
}

export default function DiffPage({ params }: DiffPageProps) {
  const { id } = params;
  const searchParams = useSearchParams();
  const router = useRouter();

  // URLからfromとtoのバージョンを取得
  const fromVersion = searchParams.get('from');
  const toVersion = searchParams.get('to');

  // APIフックを使用してデータを取得
  const { getDocument, getDocumentDiff } = useDocuments();
  const documentQuery = getDocument(id);

  // 差分データを取得
  const diffQuery = fromVersion && toVersion
    ? getDocumentDiff(id, { from_version: fromVersion, to_version: toVersion })
    : null;

  // fromまたはtoパラメータがない場合はドキュメント詳細ページにリダイレクト
  useEffect(() => {
    if (!fromVersion || !toVersion) {
      router.push(`/documents/${id}`);
    }
  }, [fromVersion, toVersion, id, router]);

  // ローディング表示
  if (documentQuery.isLoading || (diffQuery && diffQuery.isLoading)) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // エラー表示
  if (documentQuery.isError || (diffQuery && diffQuery.isError)) {
    return (
      <div className="p-6 bg-red-50 text-red-700 rounded-md max-w-4xl mx-auto mt-8">
        <h2 className="text-xl font-bold mb-2">エラーが発生しました</h2>
        <p>{'ドキュメントの差分取得に失敗しました'}</p>
        <div className="mt-4">
          <Link
            href={`/documents/${id}`}
            className="text-blue-600 hover:text-blue-800"
          >
            ドキュメント詳細に戻る
          </Link>
        </div>
      </div>
    );
  }

  // ドキュメントまたは差分データが存在しない場合
  if (!documentQuery.data || !diffQuery || !diffQuery.data) {
    return (
      <div className="p-6 bg-yellow-50 text-yellow-700 rounded-md max-w-4xl mx-auto mt-8">
        <h2 className="text-xl font-bold mb-2">差分データが見つかりません</h2>
        <p>指定されたバージョン間の差分データを取得できませんでした。</p>
        <div className="mt-4">
          <Link
            href={`/documents/${id}`}
            className="text-blue-600 hover:text-blue-800"
          >
            ドキュメント詳細に戻る
          </Link>
        </div>
      </div>
    );
  }

  const document = documentQuery.data;
  const diffData = diffQuery.data;

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Link
            href={`/documents/${id}`}
            className="text-blue-600 hover:text-blue-800"
          >
            ← ドキュメント詳細に戻る
          </Link>
        </div>

        <h1 className="text-3xl font-bold mb-2">{document.title}</h1>
        {document.description && (
          <p className="text-gray-600 mb-4">{document.description}</p>
        )}
      </div>

      <div className="bg-white shadow-md rounded-lg p-6">
        <DiffViewer diff={diffData} />
      </div>
    </div>
  );
}
